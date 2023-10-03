"""Create and write to a sqlite database. Our schema is one table per database
because it goes well with out data "lake" (drops: https://github.com/dansteingart/drops).
"""

import json
import sqlite3
from time import time
from typing import Dict, List, Union

import numpy as np

from unplugged import constants

Payload = Union[float, int, np.ndarray]


class Database:
    """Writes to a local database that is synced with drops using syncthing.

    Attributes:
        self.client: The mqtt-client responsible for starting and
            maintaining the connection.

    Example:
        db = database.Database(machine='brix2', path='INL_GT_DE_2022_08_01_1')
        while *data is being updated*:
            db.write(payload, table)
    """

    def __init__(self, db_filename: str, table_initializer: str):
        """
        Args:
            db_filename (str): Generally stick to experiment ID.
        """

        database: str = f'{constants.DATA_DIRECTORY}/{db_filename}.sqlite3'
        self.connection = sqlite3.connect(database=database)
        self.cursor = self.connection.cursor()
        self.cursor.execute(table_initializer)

    def close(self):
        self.connection.close()


class Acoustics(Database):
    table_initializer = '''CREATE TABLE IF NOT EXISTS acoustics (
        time REAL PRIMARY KEY,
        amps BLOB,
        metadata TEXT
    )
    '''
    keys = ['time, amps']  # Should be like this. We only write metadata once but the other multiple times.
    table = 'acoustics'

    def __init__(self, jig: str, exp_id: str):
        path = f'{jig}/{exp_id}'
        super().__init__(
            db_filename=path,
            table_initializer=Acoustics.table_initializer
        )
        self._set_query()

    @staticmethod
    def _parse_parameters(parameters: List[Payload]) -> tuple:
        parsed = list()

        for parameter in parameters:
            if isinstance(parameter, list):
                parsed.append(
                   sqlite3.Binary(np.array(parameter, dtype=np.float16))
                )
                continue

            parsed.append(parameter)

        return tuple(parsed)
    
    def _set_query(self) -> None:
        """Prepares the query scaffolding."""

        keys_parsed: str = ', '.join([key for key in Acoustics.keys])
        
        # The ?, ? is flaky in case I ever add more keys. I did set this programmatically
        # (see e.g. Sfogliatella) but I actually think it's more bug-prone because it's
        # uber unreadable.
        self._query = f'INSERT INTO {Acoustics.table} ({keys_parsed}) VALUES (?, ?)'
    
    def write(self, payload: Dict[str, Payload]):
        """Writes data out to Drops.


        """

        parameters = self._parse_parameters(parameters=list(payload.values()))
        self.cursor.execute(self._query, parameters)
        self.connection.commit()

        return self.cursor.lastrowid


class Metadata(Database):
    table_initializer = '''CREATE TABLE IF NOT EXISTS metadata (
        time REAL PRIMARY KEY,
        metadata TEXT
    )
    '''
    table = 'metadata'
    keys = 'time, metadata'

    def __init__(self):
        super().__init__(
            db_filename='metadata',
            table_initializer=Metadata.table_initializer
        )
        self._set_query()

    def _set_query(self):
        self._query: str = f'INSERT INTO {Metadata.table} ({Metadata.keys}) VALUES (?, ?)'

    def read_most_recent_row(self):
        query: str = f'SELECT * FROM {Metadata.table} ORDER BY time DESC LIMIT 1'
        self.cursor.execute(query)
        self.cursor.row_factory = sqlite3.Row

        result = self.cursor.fetchone()

        return dict(result)

    def write(self, meta: dict) -> None:
        metadata_json: str = json.dumps(meta)
        self.cursor.execute(self._query, (time(), metadata_json,))
        self.connection.commit()

        return self.cursor.lastrowid
