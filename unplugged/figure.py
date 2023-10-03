"""Hook for plotting test pulse results."""

from dataclasses import asdict
from datetime import datetime
from time import time

import matplotlib.pyplot as plt
import numpy as np
from pytz import timezone

from unplugged import boilerplate, constants


def _plot(ax, waveform, jig: boilerplate.Jig):
    delay = float(jig.mode.picoscope.delay)
    duration = float(jig.mode.picoscope.duration)
    t = np.linspace(delay, delay+duration, len(waveform))
    
    ax.plot(t, waveform, '#0033a0', linewidth=2)
    ax.set_xlim(t[0], t[-1])
    ax.set_xlabel("Time (us)")

    tz = timezone('EST')
    now_ = datetime.now(tz)
    now_str = now_.strftime("%Y-%m-%d %H:%M:%S")
    text_ = f'dt: {now_str}\njig: {jig.name}\n'
    
    for key, val in asdict(jig.mode.picoscope).items():
        text_ += key + ': ' + str(val) + '\n'
    
    text_ += f'gain (dB): {str(jig.mode.pulser.gain_dB)}\n'

    ax.text(
        x=delay+0.2,
        y=max(waveform),
        s=text_,
        fontsize=5,
        ha='left',
        va='top'
    )   
    plt.tight_layout()


def plot(waveform: list, jig: boilerplate.Jig) -> None:
    """Testing figure. Bad code but whatever.
    
    Args:
        data (list): The pulsing data as a list.
        PulsingParams_ (PulsingParams): Pulsing parameters,
            see definition at top of file.
    """

    fig, ax = plt.subplots(figsize=(3, 2), dpi=200, sharey=True)
    _plot(ax=ax, waveform=waveform, jig=jig)
    now = time()
    fig_name = f'{constants.DATA_DIRECTORY}/{jig.name}/pulse_{round(now)}.png'
    plt.savefig(fig_name, format='png')
    plt.clf()
