import json
import pandas as pd
from pathlib import Path
from airtable import Airtable

from utils.collective_action import CollectiveActions, CollectiveAction
from utils.files import get_all_files
from utils.misc import ca_json_converter, README, CSV, JSON, ACTION_FOLDER
from utils.markdown import update_markdown_document

"""
These functions gets Union Records
from any format (CSV, JSON, Folder)
"""

def get_urs_from_airtable(secret: str, app: str, table: str):
    """ Get CAS from airtable. """
    urs = UnionRecords()
    airtable = Airtable(app, table, api_key=secret)
    pages = airtable.get_iter(maxRecords=1000)
    records = []
    for page in pages:
        for record in page:
            records.append(record["fields"])
    for record in records:
        if bool(record):
            urs.append(
                UnionRecord(**record)
            )
    return urs


"""
These functions gets CollectiveActions
from any format (CSV, JSON, Folder)
"""

def get_cas_from_airtable(secret: str, app: str, table: str):
    """ Get CAS from airtable. """
    cas = CollectiveActions()
    airtable = Airtable(app, table, api_key=secret)
    pages = airtable.get_iter(maxRecords=1000)
    records = []
    for page in pages:
        for record in page:
            records.append(record["fields"])
    for record in records:
        if bool(record):
            cas.append(
                CollectiveAction(**record)
            )
    return cas

def get_cas_from_files(folder_path: str = ACTION_FOLDER):
    """ Get CAS from action files. """
    files = get_all_files(folder_path)
    return CollectiveActions.read_from_files(files, folder=folder_path).sort()


def get_cas_from_csv(csv_path: str = CSV):
    """ Get CAS from CSV. """
    df = pd.read_csv(csv_path)
    return CollectiveActions.read_from_df(df).sort()


def get_cas_from_json(json_path: str = JSON):
    """ Get CAS from JSON. """
    df = pd.read_json(json_path)
    return CollectiveActions.read_from_df(df).sort()


"""
These functions saves CollectiveActions
to any format (CSV, JSON, Folder, README)
"""


def save_cas_to_files(
    cas: CollectiveActions, folder_path: str = ACTION_FOLDER
):
    """ Save CAS to action folder. """
    cas.to_files(folder=folder_path)


def save_cas_to_readme(cas: CollectiveActions, readme_path: str = README):
    """ Save CAS to README.md. """
    readme = Path(readme_path)
    md_document = readme.read_text()
    md_document = update_markdown_document(
        md_document, CollectiveActions.ca_id, cas
    )
    readme.write_text(md_document)


def save_cas_to_csv(cas: CollectiveActions, csv_path: str = CSV):
    """ Save CAS to CSV. """
    df = cas.to_df()
    df.to_csv(csv_path)


def save_cas_to_json(cas: CollectiveActions, json_path: str = JSON):
    """ Save CAS to JSON. """
    data = cas.to_dict()
    with open(str(json_path), "w") as outfile:
        json.dump(data, outfile, default=ca_json_converter, indent=4)
