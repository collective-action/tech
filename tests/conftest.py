import pytest
import pandas as pd
from pathlib import Path
from utils.action import CollectiveAction, CollectiveActions
from tempfile import TemporaryDirectory


@pytest.fixture(scope="session")
def tmp_session(tmp_path_factory):
    """ Same as 'tmp' fixture but with session level scope. """
    with TemporaryDirectory(dir=tmp_path_factory.getbasetemp()) as td:
        yield td


@pytest.fixture(scope="session")
def correctly_formatted_ca_file(tmp_session) -> str:
    """ Return a markdown string for of a single action. This is what we've
    expect to see in one of the files under the /actions folder."""
    msg = """
- date: 2019-04-10
- sources: https://www.your.valid/source1, https://www.your.valid/source2
- companies: amazon
- actions: open_letter
- struggles: ethics
- workers: 1000
- description: Thousands of people protest a military contract in Queens.
- locations: new_york
- tags: military_contract
- author: organizejs
"""
    action = Path(tmp_session) / "0001.md"
    action.write_text(msg)
    return action


@pytest.fixture(scope="session")
def correctly_formatted_cas_files(tmp_session) -> str:
    """ Return a markdown string for of a single action. This is what we've
    expect to see in one of the files under the /actions folder."""
    msg1 = """
- date: 2019-04-10
- sources: https://www.your.valid/source1, https://www.your.valid/source2
- companies: amazon
- actions: open_letter
- struggles: ethics
- workers: 1000
- description: Thousands of people protest a military contract in Queens.
- locations: new_york
- tags: military_contract
- author: organizejs
"""
    msg2 = """
- date: 2019-04-04
- sources: https://www.wired.com/story/microsoft-employees-protest-treatment-women-ceo-nadella/
- actions: protest, open_letter
- struggles: discrimination
- description: A group of Microsoft employees appeared at an employee meeting with CEO Satya Nadella Thursday to protest the companies's treatment of women. It's not clear how many were part of the protest, but some female and male employees at the event wore all white, inspired by the congresswomen who wore suffragette white to the State of the Union in February.
- locations: seattle
- companies: microsoft
- author: organizejs
"""
    msg3 = """
- date: 2019-04-02
- sources: https://www.theguardian.com/technology/2019/apr/02/google-workers-sign-letter-temp-contractors-protest
- actions: open_letter
- struggles: working_conditions, pay_and_benefits
- description: More than 900 Google workers have signed a letter objecting to the tech giant's treatment of temporary contractors, in what organizers are calling a 'historical coalition' between Google's full-time employees (FTEs) and temps, vendors and contractors (TVCs).
- locations: online
- companies: google
- author: organizejs
"""
    ca1 = Path(tmp_session) / "0001.md"
    ca2 = Path(tmp_session) / "0002.md"
    ca3= Path(tmp_session) / "0003.md"

    ca1.write_text(msg1)
    ca2.write_text(msg2)
    ca3.write_text(msg3)

    return [ca1, ca2, ca3]


@pytest.fixture(scope="session")
def correctly_formatted_ca_series() -> pd.Series:
    """ Return a markdown string for the tests to use. """
    return pd.Series(
        {
            "author": "organizejs",
            "date": "2019-04-10",
            "sources": "https://www.recode.net/2019/4/10/18304877/amazon-climate-change-employees-tech-activism",
            "actions": "open_letter",
            "struggles": "ethics",
            "description": "More than 3,500 of the company's corporate employees signed their names to a letter published on Wednesday that urged Jeff Bezos to create a comprehensive climate-change plan for the company.",
            "locations": "online",
            "companies": "amazon",
            "workers": 4000,
            "tags": "environmental",
        }
    )


@pytest.fixture(scope="session")
def correctly_formatted_cas_df():
    """ Return a dataframe for the tests to use. """
    return pd.DataFrame(
        [
            {
                "author": "organizejs",
                "date": "2019-04-10",
                "sources": "https://www.recode.net/2019/4/10/18304877/amazon-climate-change-employees-tech-activism",
                "actions": "open_letter",
                "struggles": "ethics",
                "description": "More than 3,500 of the company's corporate employees signed their names to a letter published on Wednesday that urged Jeff Bezos to create a comprehensive climate-change plan for the company.",
                "locations": "online",
                "companies": "amazon",
                "workers": 4000,
                "tags": "environmental",
            },
            {
                "author": "organizejs",
                "date": "2019-04-04",
                "sources": "https://www.wired.com/story/microsoft-employees-protest-treatment-women-ceo-nadella/",
                "actions": "protest",
                "struggles": "discrimination",
                "description": "A group of Microsoft employees appeared at an employee meeting with CEO Satya Nadella Thursday to protest the companies's treatment of women. It's not clear how many were part of the protest, but some female and male employees at the event wore all white, inspired by the congresswomen who wore suffragette white to the State of the Union in February.",
                "locations": "seattle",
                "companies": "microsoft",
            },
            {
                "author": "organizejs",
                "date": "2019-04-02",
                "sources": "https://www.theguardian.com/technology/2019/apr/02/google-workers-sign-letter-temp-contractors-protest",
                "actions": ["open_letter", "protest"],
                "struggles": ["working_conditions", "pay_and_benefits"],
                "description": "More than 900 Google workers have signed a letter objecting to the tech giant's treatment of temporary contractors, in what organizers are calling a 'historical coalition' between Google's full-time employees (FTEs) and temps, vendors and contractors (TVCs).",
                "locations": "online",
                "companies": "google",
                "workers": 900,
            },
        ]
    )

