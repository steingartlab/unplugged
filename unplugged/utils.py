import os
from time import time
from typing import Union

from unplugged import constants


def _most_recent(jig, filetype) -> tuple[float, str]:
    latest_time = 0.0
    latest_file = None

    directory = f'{constants.DATA_DIRECTORY}/{jig}'
    does_exist = os.path.exists(directory)

    if not does_exist:
        os.makedirs(directory, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.endswith(filetype):
            filepath = os.path.join(directory, filename)
            file_time = os.path.getmtime(filepath)
            
            if file_time > latest_time:
                latest_time = file_time
                latest_file = filepath

    return latest_time, latest_file


def check_when_last_updated(jig: str) -> Union[float,str]:
    latest_time, _ = _most_recent(jig, filetype='sqlite3')

    time_since_last_updated = time() - latest_time

    if time_since_last_updated > 1.6e9:
        return 'inf'
    
    return round(time_since_last_updated, 1)


def get_most_recent_png(jig) -> Union[str, None]:
    _, latest_file = _most_recent(jig, filetype='png')
    
    if latest_file is None:
        return

    return latest_file
