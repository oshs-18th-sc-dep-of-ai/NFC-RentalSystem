"""
From https://github.com/oshs-17th-sc-dep-of-ai/urban-fishstick/
    backend/src/util/json_util.py
    by Chae Yool
"""

from typing import Any
import json


def read_json(path: str) -> Any:
    with open(path, 'r') as fs:
        return json.load(fs)


def write_json(path: str, obj: Any) -> None:
    with open(path, 'w') as fs:
        json.dump(obj, fs)