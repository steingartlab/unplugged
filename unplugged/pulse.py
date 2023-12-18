"""For sending test pulses to gauge SNR."""

from time import sleep
import traceback


from unplugged import boilerplate, constants, mux, picoscope, pulser, slack

def _sleep(sleep_s: float = 0.05):
    sleep(sleep_s)

def _pulse(mode: boilerplate.Mode):
    print('\tpulse')
    pulser.turn_on()
    pulser.set_properties(mode.pulser)
    _sleep()  # Needed! For the pulser to switch

    mux.clear()
    mux.latch(channel=mode.mux_channel)
    _sleep()  # Needed! For the mux to switch

    raw = picoscope.callback(mode.picoscope)

    pulser.turn_off()

    return raw[constants.WAVEFORM_COL][0]


def pulse(mode: boilerplate.Mode) -> list[float]:
    try:
        return _pulse(mode)

    except Exception as e:
        traceback_details = traceback.format_exc()
        print(traceback_details)
        slack.post(message=f"Unplugged: ```{traceback_details}```")
