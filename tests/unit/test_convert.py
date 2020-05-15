import pytest
import os
from utils.convert import (
    get_cas_from_files,
    get_cas_from_csv,
    get_cas_from_json,
    save_cas_to_files,
    save_cas_to_readme,
    save_cas_to_csv,
    save_cas_to_json,
)


@pytest.fixture(scope="session")
def cas(action_folder_path):
    return get_cas_from_files(folder_path=action_folder_path)


def test_get_cas_from_files(action_folder_path):
    get_cas_from_files(folder_path=action_folder_path)


def test_get_cas_from_csv(csv_path):
    print(csv_path)
    get_cas_from_csv(csv_path=csv_path)


def test_get_cas_from_json(json_path):
    get_cas_from_json(json_path=json_path)


def test_save_cas_to_files(cas, tmp_session):
    save_cas_to_files(cas, folder_path=tmp_session)


def test_save_cas_to_readme(cas, readme_path):
    save_cas_to_readme(cas, readme_path=readme_path)


def test_save_cas_to_csv(cas, tmp_session):
    fp = os.path.join(tmp_session, "actions.csv")
    open(fp, "w").close()  # create new file
    save_cas_to_csv(cas, csv_path=fp)


def test_save_cas_to_json(cas, tmp_session):
    fp = os.path.join(tmp_session, "actions.json")
    open(fp, "w").close()  # create new file
    save_cas_to_json(cas, json_path=fp)
