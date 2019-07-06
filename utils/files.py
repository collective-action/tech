import os
import glob
from pathlib import Path

class FileClient:
    """ This class manages the file system of Actions. """

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
                    os.path.dirname(__file__),
                    os.path.pardir,
                    "actions"
                )
            )
        )

    def save_to_file(self, filename: str, action: dict) -> None:
        """ Serialize action from json to txt file. """
        text = ""
        for key, value in action.items():
            text += key + ": "
            text += value + "\n"
        f = open(self.actions_folder/filename, "w")
        f.write(text)
        f.close()

    @staticmethod
    def read_from_file() -> "Actions":
        """ Parses files and generates an Actions object. """
        pass

    def remove_actions(self) -> None:
        """ Removes all actions from list of files. """
        files = glob.glob(str(self.actions_folder/"*.txt"))
        for file in files:
            os.remove(file)
