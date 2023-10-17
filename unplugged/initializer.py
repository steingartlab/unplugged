"""For setting up the unplugged folder structure and dummy files."""

import os
import shutil

from unplugged import constants, database


# # Create a dummy sqlite file
DB_FILENAME = 'metadata'
DIRECTORY_NAME = 'data'
DATABASE_PATH: str = f'{DIRECTORY_NAME}/{DB_FILENAME}.sqlite3'
METADATA_TABLE_INTIIALIZER = '''CREATE TABLE IF NOT EXISTS metadata (
        time REAL PRIMARY KEY,
        metadata TEXT
    )
'''
IMAGE_FOLDER = 'static'
STARTUP_IMAGE = 'startup_image.png'
DUMMY_INITIAL_METADATA = {
    "jig": {
        "user": "gunnar",
        "exp_id": "test_0",
        "delay": 10,
        "duration": 10,
        "voltage_range": 1,
        "avg_num": 32,
        "gain_dB": 30,
        "mux_row": 7,
        "status": "idling"
    },
}

def _create_database() -> None:
    if os.path.exists(DATABASE_PATH):
        print(f"Dummy file exists for folder {DATABASE_PATH}")
        
        return
    
    db = database.Metadata()

    dummy_metadata = dict()

    for jig in constants.JIGS:
        dummy_metadata[jig] = DUMMY_INITIAL_METADATA['jig']

    db.write(dummy_metadata)


def _add_image(new_directory) -> None:
    image_directory = f'{new_directory}/{STARTUP_IMAGE}'

    if os.path.exists(image_directory):
        print(f"Image exists for directory {new_directory}")
        return

    source_path = f'{IMAGE_FOLDER}/{STARTUP_IMAGE}'
    shutil.copy(source_path, new_directory)


def _create_jig_folders() -> None:
    jigs = constants.JIGS

    for jig_name in jigs:
        new_directory = os.path.join(os.getcwd(), DIRECTORY_NAME, jig_name)
        
        if os.path.exists(new_directory):
            print(f"Folder exists for jig {jig_name}")
            continue

        os.makedirs(new_directory)
        _add_image(new_directory)


def initialize():
    os.makedirs(DIRECTORY_NAME, exist_ok=True)
    _create_database()
    _create_jig_folders()






