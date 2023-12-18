"""For sending test pulses to gauge SNR."""

from time import sleep
import traceback


from unplugged import boilerplate, constants, mux, picoscope, pulser, slack


def _pulse(mode: boilerplate.Mode):
    pulser.turn_on()
    pulser.set_properties(mode.pulser)
    sleep(0.1)  # Needed! For the pulser to switch

    mux.clear()
    sleep(0.1)  # Needed! For the mux to switch
    mux.latch(channel=mode.mux_channel)
    sleep(0.1)  # Needed! For the mux to switch

    raw = picoscope.callback(mode.picoscope)

    pulser.turn_off()

    return raw[constants.WAVEFORM_COL][0]


def pulse(mode: boilerplate.Mode) -> list[float]:
    try:
        return _pulse()

    except Exception as e:
        traceback_details = traceback.format_exc()
        print(traceback_details)
        slack.post(message=f"Unplugged: ```{traceback_details}```")
