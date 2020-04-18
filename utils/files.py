import os
import glob
import json
from typing import List
from pathlib import Path
from utils.misc import ca_json_converter


class FileClient:
    """ This class manages the file system of Actions.

    When serializing or deserializing, it will assume the following format:
    ```json
    {
      <field1>: [<value1>, <value2>]
      <field2>: <value2>
    }
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
        f = open(filepath, "w")
        json.dump(ca, f, default=ca_json_converter)
        f.close()

    def get_all_files(self) -> List[Path]:
        """ Get all the files in the actions folder. """
        return [
            f
            for f in os.listdir(self.cas_folder)
            if os.path.isfile(os.path.join(self.cas_folder, f))
            and f.lower().endswith(".json")
        ]

    def parse_file(self, filepath: str) -> dict:
        """ Parses a file in the actions folder and returns dict. """
        f = open(filepath, "r")
        return json.load(f)

    def remove_all_files(self) -> None:
        """ Removes all actions from list of files. """
        files = glob.glob(str(self.cas_folder / "*.json"))
        for file in files:
            os.remove(file)
