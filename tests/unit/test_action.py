from utils.action import Action, Actions
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
    assert action.action == "petition" # test regular field
    assert action.struggles == ["ethics"] # test list field


def _test_actions(actions: Actions):
    assert len(actions) == 3
    assert actions.actions[0].author == "organizejs"


def test_action_create_from_md(correctly_formatted_md_action):
    """ Test Action `create_from_md` function. """
    soup = BeautifulSoup(correctly_formatted_md_action, "html.parser")
    action = Action.create_from_md(soup.table)
    _test_action(action)


def test_action_create_from_row(correctly_formatted_series_action):
    """ Test Action `create_from_row` function. """
    action = Action.create_from_row(correctly_formatted_series_action)
    _test_action(action)


def test_actions_read_from_md(correctly_formatted_md_actions):
    """ Test Actions `read_from_md` function. """
    actions = Actions.read_from_md(correctly_formatted_md_actions)
    _test_actions(actions)


def test_actions_read_from_df(correctly_formatted_df_actions):
    """ Test Actions `read_from_df` function. """
    actions = Actions.read_from_df(correctly_formatted_df_actions)
    _test_actions(actions)


def test_correctly_formatted_md_and_series_action_fixtures(
    correctly_formatted_series_action, correctly_formatted_md_action
):
    """ Test that fixtures equal each other. They should! """
    action_from_df = Action.create_from_row(correctly_formatted_series_action)
    action_from_md = Action.create_from_md(BeautifulSoup(correctly_formatted_md_action,
        "html.parser").table)
    assert action_from_df == action_from_md


def test_correctly_formatted_md_and_df_actions_fixtures(
    correctly_formatted_df_actions, correctly_formatted_md_actions
):
    """ Test that fixtures equal each other. They should! """
    actions_from_df = Actions.read_from_df(correctly_formatted_df_actions)
    actions_from_md = Actions.read_from_md(correctly_formatted_md_actions)
    assert actions_from_df == actions_from_md


def test_actions_to_md(correctly_formatted_df_actions):
    """ Test Actions `to_md` function. """
    actions_from_df = Actions.read_from_df(correctly_formatted_df_actions)
    actions_as_md = actions_from_df.to_md()
    s1 = BeautifulSoup(actions_as_md, 'html.parser')
    assert len(s1.div.find_all("table")) == 3


def test_actions_to_df(correctly_formatted_md_actions):
    """ Test Actions `to_df` function. """
    actions_from_md = Actions.read_from_md(correctly_formatted_md_actions)
    actions_as_df = actions_from_md.to_df()
    assert len(actions_as_df) == 3
    assert isinstance(actions_as_df, pd.DataFrame)


def test_actions_sort(correctly_formatted_df_actions):
    """ Test that Actions is sortable. """
    actions_from_df = Actions.read_from_df(correctly_formatted_df_actions)
    sorted_actions = actions_from_df.sort()
    assert sorted_actions.actions[0].date == dateparser.parse("2019-04-02").date()
    reverse_sorted_actions = actions_from_df.sort(reverse=True)
    assert reverse_sorted_actions.actions[0].date == dateparser.parse("2019-04-10").date()
