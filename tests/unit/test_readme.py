from utils.action import Action, Actions
from convert import README_PATH
from pathlib import Path

def test_readme():
    """ Test that all input in the readme is valid. """
    readme = Path(README_PATH).read_text()
    Actions.read_from_md(readme)

