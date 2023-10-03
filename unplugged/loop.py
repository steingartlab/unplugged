"""The main control loop. Creates a queue of jigs that are 
executed in turn.
"""

from time import time

from unplugged import (
    boilerplate,
    controller,
    database,
    figure,
    mux,
    picoscope,
    pulse,
    pulser,
    slack
)


def _loop(jig: boilerplate.Jig):
    if jig.status == boilerplate.Status.idling:
        return

    payload = {'time': time()}
    payload['waveform'] = pulse.pulse(jig.mode)

    if jig.status == boilerplate.Status.pulsing:
        figure.plot(payload['waveform'], jig.mode)
        return
    
    database_ = database.Acoustics(db_filename=jig.exp_id)
    database_.write(payload)
    database_.close()


def loop():
    meta = controller.load_most_recent_meta()
    for name, params in meta.items():        
        mode = boilerplate.Mode(
            pulser=pulser.Pulser(params['gain_dB']),
            mux_channel=mux.Channel(row=params['mux_row']),
            picoscope=picoscope.Picoscope(
                delay=params['delay'],
                duration=params['duration'],
                voltage_range=params['voltage_range'],
                avg_num=params['avg_num']
            ),
        )
        jig = boilerplate.Jig(
            name=name,
            status=params['status'],
            exp_id=params['exp_id'],
            mode=mode
        )

        try:
            _loop(jig)
            
        except Exception as e:
            slack.post(message=f"Unplugged: ```{e}```")
            continue