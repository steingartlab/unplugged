"""Creates a continuous loop that runs the jig queue every 5 seconds.

Decided on doing this over a cronjob because it's easier to execute
in a container — this script can act as an entrypoint.
"""

import schedule
import time

from unplugged import constants, loop

def main():
    schedule.every(constants.SLEEP_BETWEEN_LOOPS_S).seconds.do(loop.loop)

    while True:
        schedule.run_pending()
        time.sleep(0.5)


