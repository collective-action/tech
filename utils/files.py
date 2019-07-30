import os
import glob
from typing import List
from pathlib import Path


class FileClient:
    """ This class manages the file system of Actions.

    When serializing or deserializing, it will assume the following format:
    ```md
    - <field1>: <value1>
    - <field2>: <value2>
    ```
    """

    actions_folder = ""

    def __init__(self):
        """ Setup i/o stuff """
        self.actions_folder = self.get_actions_folder()

    @staticmethod
    def get_actions_folder() -> Path:
        """ Get the absolute path of the folder to put actions in. """
        return Path(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), os.path.pardir, "actions"
                )
            )
        )

    def save_to_file(self, filepath: str, action: dict) -> None:
        """ Serialize action from json to md file. """
        text = ""
        for key, value in action.items():
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
            for f in os.listdir(self.actions_folder)
            if os.path.isfile(os.path.join(self.actions_folder, f))
            and f.lower().endswith(".md")
        ]

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
        files = glob.glob(str(self.actions_folder / "*.md"))
        for file in files:
            os.remove(file)
