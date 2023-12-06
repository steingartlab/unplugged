import ast
import json
from typing import Callable

from unplugged import constants, database, initializer, utils


def _load_most_recent_meta():
    database_ = database.Metadata()
    most_recent_meta = database_.read_most_recent_row()
    database_.close()

    return most_recent_meta["metadata"]


def load_most_recent_meta() -> dict:
    meta = json.loads(_load_most_recent_meta())

    for jig_name in constants.JIGS:
        if jig_name not in meta:
            meta[jig_name] = initializer.DUMMY_INITIAL_METADATA["jig"]

    return meta


def write_meta(updated_jigs: dict) -> None:
    most_recent_meta: dict = ast.literal_eval(_load_most_recent_meta())
    meta = most_recent_meta.copy()

    for jig_name, jig_meta in updated_jigs.items():
        meta[jig_name] = jig_meta

    database_ = database.Metadata()
    database_.write(meta)
    database_.close()


def _load_most_recent(fn: Callable) -> dict:
    most_recent = dict()

    for jig in constants.JIGS:
        most_recent[jig] = fn(jig)

    return most_recent


def load_most_recent_timestamps() -> dict[str, float]:
    return _load_most_recent(utils.check_when_last_updated)


def load_most_recent_images() -> dict[str, bytes]:
    return _load_most_recent(utils.get_most_recent_png)
