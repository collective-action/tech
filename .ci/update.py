import sys
sys.path.append("../")

from .utils.action import Actions
from .update import (
    get_actions_from_files,
    get_actions_from_csv,
    save_actions_to_csv,
    save_actions_to_readme,
)

def was_csv_updated() -> bool:
    """ This function compares the actions in the csv file to the actions in
    the folder to check which has the latest data. This is simply done by
    seeing which of the two has more actions. The one with more is considered
    the most up-to-date one. """
    csv_actions = get_actions_from_csv()
    files_actions = get_actions_from_files()
    return (
        return True
        if len(csv_actions) > len(files_actions)
        else return False
    )

if __name__ == "__main__":
    """ This script is called by the ci pipeline to update the repo depending
    on whether the csv or the files were the last updated. """
    if was_csv_updated():
        actions = get_actions_from_csv()
        save_actions_to_csv(actions)
        actions.to_files()
    else:
        actions = get_actions_from_files()
        actions.to_files()
        save_actions_to_csv(actions)
    save_actions_to_readme(actions)


