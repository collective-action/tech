import pytest
import os
from pathlib import Path
from tempfile import TemporaryDirectory


TEST_ACTION_FOLDER = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, "resources/test_actions"
        )
    )
)


TEST_CSV = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, "resources/test_actions.csv"
        )
    )
)


TEST_JSON = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, "resources/test_actions.json"
        )
    )
)


TEST_README = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, "resources/README.md"
        )
    )
)


@pytest.fixture(scope="session")
def action_folder_path():
    return TEST_ACTION_FOLDER


@pytest.fixture(scope="session")
def csv_path():
    return TEST_CSV


@pytest.fixture(scope="session")
def json_path():
    return TEST_JSON


@pytest.fixture(scope="session")
def readme_path():
    return TEST_README


@pytest.fixture(scope="session")
def tmp_session(tmp_path_factory):
    """ Same as 'tmp' fixture but with session level scope. """
    with TemporaryDirectory(dir=tmp_path_factory.getbasetemp()) as td:
        yield td
