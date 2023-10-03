"""For sending test pulses to gauge SNR."""

from time import sleep


from unplugged import boilerplate, constants, mux, picoscope, pulser



def pulse(mode: boilerplate.Mode) -> list[float]:
    pulser.turn_on()
    pulser.set_properties(mode.pulser)
    sleep(0.1)  # Needed! For the pulser to switch
    
    mux.clear()
    mux.latch(channel=mode.mux_channel)
    sleep(0.1)  # Needed! For the mux to switch
    
    raw = picoscope.callback(mode.picoscope)
    
    mux.unlatch(channel=mode.mux_channel)
    pulser.turn_off()
    
    return raw[constants.WAVEFORM_COL][0]    
    