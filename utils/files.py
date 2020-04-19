import os
import glob
import json
from typing import List
from pathlib import Path
from utils.misc import ca_json_converter


""" These functions are helpers for dealing with action files

When serializing or deserializing, it will assume the following format:
```json
{
  <field1>: [<value1>, <value2>]
  <field2>: <value2>
}
```
"""


def save_to_file(filepath: str, ca: dict) -> None:
    """ Serialize action from json to md file. """
    f = open(filepath, "w")
    json.dump(ca, f, default=ca_json_converter, indent=4)
    f.close()


def get_all_files(folder: Path) -> List[Path]:
    """ Get all the files in the actions folder. """
    return [
        f
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f.lower().endswith(".json")
    ]


def parse_file(filepath: str) -> dict:
    """ Parses a file in the actions folder and returns dict. """
    f = open(filepath, "r")
    return json.load(f)


def remove_all_files(folder: Path) -> None:
    """ Removes all actions from list of files. """
    files = glob.glob(str(Path(folder) / "*.json"))
    for file in files:
        os.remove(file)
