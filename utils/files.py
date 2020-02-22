import os
import glob
from typing import List
from pathlib import Path
import datetime


def get_last_modified(filepath: str) -> datetime:
    """ Get the last modified datetime of a file """
    t = os.path.getmtime(filepath)
    return datetime.datetime.fromtimestamp(t)


class FileClient:
    """ This class manages the file system of Actions.

    When serializing or deserializing, it will assume the following format:
    ```md
    - <field1>: <value1>
    - <field2>: <value2>
    ```
    """

    cas_folder = ""

    def __init__(self):
        """ Setup i/o stuff """
        self.cas_folder = self.get_cas_folder()

    @staticmethod
    def get_cas_folder() -> Path:
        """ Get the absolute path of the folder to put actions in. """
        return Path(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), os.path.pardir, "actions"
                )
            )
        )

    def save_to_file(self, filepath: str, ca: dict) -> None:
        """ Serialize action from json to md file. """
        text = ""
        for key, value in ca.items():
            text += "- "
            text += key + ": "
            text += value + "\n"
        f = open(filepath, "w")
        f.write(text)
        f.close()

    def get_all_files(self) -> List[Path]:
        """ Get all the files in the actions folder. """
        return [
            f
            for f in os.listdir(self.cas_folder)
            if os.path.isfile(os.path.join(self.cas_folder, f))
            and f.lower().endswith(".md")
        ]

    def get_datetime_of_last_modified_file(self) -> datetime:
        """ Gets the datetime of the most recently updated file. """
        files = self.get_all_files()
        most_recent_dt = datetime.datetime(2000, 1, 1)
        for f in files:
            dt = get_last_modified(self.cas_folder / f)
            if dt > most_recent_dt:
                most_recent_dt = dt
        return most_recent_dt

    def parse_file(self, filepath: str) -> dict:
        """ Parses a file in the actions folder and returns dict. """
        f = open(filepath, "r")
        contents = f.read().strip()
        d = {}
        for row in contents.split("\n"):
            if len(row) > 0:
                key = row.split(": ", 1)[0][1:].strip()
                value = row.split(": ", 1)[1]
                d[key] = value
        return d

    def remove_all_files(self) -> None:
        """ Removes all actions from list of files. """
        files = glob.glob(str(self.cas_folder / "*.md"))
        for file in files:
            os.remove(file)
