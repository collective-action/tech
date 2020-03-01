from utils.collective_action import CollectiveAction, CollectiveActions
from utils.files import FileClient
from bs4 import BeautifulSoup
import dateparser
import pandas as pd

# ca is short for collective_action
# cas is plural for `ca`


def test_ca_constructor():
    """ Test Action constructor. """
    # test only mandatory
    CollectiveAction(
        date="2019-01-01",
        sources=["http://www.google.com"],
        actions=["strike"],
        struggles=["working_conditions"],
        employment_types=["white_collar_workers", "in_house_workers"],
        description="Foo bar.",
    )

    # test all fields
    CollectiveAction(
        date="2019-01-01",
        sources=["http://www.google.com"],
        actions=["strike"],
        struggles=["working_conditions"],
        employment_types=["white_collar_workers", "in_house_workers"],
        description="Foo bar.",
        locations=["Boston"],
        companies=["google"],
        workers=100,
        tags=["random_tag"],
        author="organizejs",
    )


def _test_ca(ca: CollectiveAction):
    assert ca.date == dateparser.parse("2019-04-10").date() # test date
    assert ca.author == "organizejs" # test meta data
    assert ca.actions == ["open_letter"] # test list field
    assert ca.struggles == ["ethics"] # test list field
    assert ca.employment_types == ["white_collar_workers", "in_house_workers"]


def _test_cas(cas: CollectiveActions):
    assert len(cas) == 3
    assert cas.cas[0].author == "organizejs"


def test_ca_create_from_file(correctly_formatted_ca_file):
    """ Test CollectiveAction `create_from_dict` function. """
    fc = FileClient()
    a = fc.parse_file(correctly_formatted_ca_file)
    ca = CollectiveAction.create_from_dict(a)
    _test_ca(ca)


def test_ca_create_from_files(correctly_formatted_cas_files):
    """ Test CollectiveActions `read_from_files` function. """
    cas = CollectiveActions.read_from_files(correctly_formatted_cas_files)
    _test_cas(cas)


def test_ca_create_from_row(correctly_formatted_ca_series):
    """ Test CollectiveAction `create_from_row` function. """
    ca = CollectiveAction.create_from_row(correctly_formatted_ca_series)
    _test_ca(ca)


def test_cas_read_from_df(correctly_formatted_cas_df):
    """ Test CollectiveActions `read_from_df` function. """
    cas = CollectiveActions.read_from_df(correctly_formatted_cas_df)
    _test_cas(cas)


def test_cas_sort(correctly_formatted_cas_df):
    """ Test that CollectiveActions is sortable. """
    cas_from_df = CollectiveActions.read_from_df(correctly_formatted_cas_df)
    sorted_cas = cas_from_df.sort()
    assert sorted_cas.cas[0].date == dateparser.parse("2019-04-02").date()
    reverse_sorted_cas = cas_from_df.sort(reverse=True)
    assert reverse_sorted_cas.cas[0].date == dateparser.parse("2019-04-10").date()
