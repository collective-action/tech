from utils.action import Action, Actions
from utils.files import FileClient
from bs4 import BeautifulSoup
import dateparser
import pandas as pd


def test_action_constructor():
    """ Test Action constructor. """
    # test only mandatory
    Action(
        date="2019-01-01",
        sources=["http://www.google.com"],
        action="strike",
        struggles=["working_conditions"],
        description="Foo bar.",
    )

    # test all fields
    Action(
        date="2019-01-01",
        sources=["http://www.google.com"],
        action="strike",
        struggles=["working_conditions"],
        description="Foo bar.",
        locations=["Boston"],
        companies=["google"],
        workers=100,
        tags=["random_tag"],
        author="organizejs",
    )


def _test_action(action: Action):
    assert action.date == dateparser.parse("2019-04-10").date() # test date
    assert action.author == "organizejs" # test meta data
    assert action.action == "open_letter" # test regular field
    assert action.struggles == ["ethics"] # test list field


def _test_actions(actions: Actions):
    assert len(actions) == 3
    assert actions.actions[0].author == "organizejs"


def test_action_create_from_file(correctly_formatted_action_file):
    """ Test Action `create_from_dict` function. """
    fc = FileClient()
    a = fc.parse_file(correctly_formatted_action_file)
    action = Action.create_from_dict(a)
    _test_action(action)


def test_action_create_from_files(correctly_formatted_action_files):
    """ Test Actions `read_from_files` function. """
    actions = Actions.read_from_files(correctly_formatted_action_files)
    _test_actions(actions)


def test_action_create_from_row(correctly_formatted_series_action):
    """ Test Action `create_from_row` function. """
    action = Action.create_from_row(correctly_formatted_series_action)
    _test_action(action)


def test_actions_read_from_df(correctly_formatted_df_actions):
    """ Test Actions `read_from_df` function. """
    actions = Actions.read_from_df(correctly_formatted_df_actions)
    _test_actions(actions)


def test_actions_sort(correctly_formatted_df_actions):
    """ Test that Actions is sortable. """
    actions_from_df = Actions.read_from_df(correctly_formatted_df_actions)
    sorted_actions = actions_from_df.sort()
    assert sorted_actions.actions[0].date == dateparser.parse("2019-04-02").date()
    reverse_sorted_actions = actions_from_df.sort(reverse=True)
    assert reverse_sorted_actions.actions[0].date == dateparser.parse("2019-04-10").date()
