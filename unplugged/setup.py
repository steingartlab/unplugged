import sqlite3
import constants
import os
import shutil

# # Create a dummy sqlite file
path = 'test_sqlite' #need to change this to match unplugged
db_filename='metadata'
database: str = f'{path}/{db_filename}.sqlite3'

if os.path.exists(database):
    print("Dummy file exists")
    exit
else:
    table_initializer = '''CREATE TABLE IF NOT EXISTS metadata (
            time REAL PRIMARY KEY,
            metadata TEXT
        )
    '''
    connection = sqlite3.connect(database=database)
    cursor = connection.cursor()
    cursor.execute(table_initializer)


# Create dummy pokemon folders
directory_name = 'acoustics_data'
jigs = constants.JIGS
for jig_name in jigs:
    new_directory = os.path.join(os.getcwd(), directory_name, jig_name)
    if os.path.exists(new_directory):
        print("Folder exists")
        exit
    else:
        os.makedirs(new_directory)
    image_directory = 'new_directory/startup_image.jpg'
    if os.path.exists(image_directory):
        print("Image exists")
        exit
    else:
        source_path = 'pokemon_startup_images/startup_image.jpg'
        shutil.copy(source_path, new_directory)








