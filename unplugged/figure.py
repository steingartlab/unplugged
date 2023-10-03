"""Hook for plotting test pulse results."""

from dataclasses import asdict
from datetime import datetime
from time import time

import matplotlib.pyplot as plt
import numpy as np
from pytz import timezone

from unplugged import boilerplate, constants


def _plot(ax, waveform, pulsing_params, jig):
    t = np.linspace(
        pulsing_params.delay,
        pulsing_params.delay+pulsing_params.duration,
        len(waveform)
    )
    
    ax.plot(t, waveform, '#0033a0', linewidth=2)
    ax.set_xlim(t[0], t[-1])
    ax.set_xlabel("Time (us)")

    if jig == 'transmission':
        ax.set_ylabel("Amplitude (V)")
    
    tz = timezone('EST')
    now_ = datetime.now(tz)
    now_str = now_.strftime("%Y-%m-%d %H:%M:%S")
    
    text_ = f'dt: {now_str}\njig: {jig}\n'

    for key, val in asdict(pulsing_params).items():
        text_ += key + ': ' + str(val) + '\n'

    ax.text(
        x=pulsing_params.delay+0.2,
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

    _plot(
        ax=ax,
        waveform=waveform,
        pulsing_params=jig.mode.picoscope,
        jig=jig.name
    )
        
    now = time()
    fig_name = f'{constants.DATA_DIRECTORY}/{jig.name}/pulse_{round(now)}.png'
    plt.savefig(fig_name, format='png')
