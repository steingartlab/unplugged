"""The main control loop. Creates a queue of jigs that are 
executed in turn.
"""

from time import sleep, time
import traceback

from unplugged import constants

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
        figure.plot(waveform=payload['waveform'], jig=jig)
        return

    database_ = database.Acoustics(exp_id=jig.exp_id, jig=jig.name)
    database_.write(payload)
    database_.close()


def loop():
    meta = controller.load_most_recent_meta()

    for name, params in meta.items():
        mode = boilerplate.Mode(
            pulser=pulser.Pulser(params['gain_dB'], mode=params['mode']),
            mux_channel=mux.Channel(
                module=params['mux_module'],
                row=params['mux_row'])
            ,
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
        _loop(jig)


def main():
    """Creates a continuous loop that runs the jig queue every 5 seconds.

    Decided on doing this over a cronjob because it's easier to execute
    in a container — this script can act as an entrypoint.
    """

    while True:
        try:
            print('external loop')
            loop()
            sleep(constants.SLEEP_BETWEEN_LOOPS_S)
        except Exception as e:
            traceback_details = traceback.format_exc()
            print(traceback_details)
            slack.post(message=f"Unplugged: ```{traceback_details}```")
            continue
