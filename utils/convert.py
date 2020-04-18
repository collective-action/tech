import json
import pandas as pd
from pathlib import Path

from utils.collective_action import CollectiveActions
from utils.files import FileClient
from utils.misc import ca_json_converter, README, CSV, JSON
from utils.markdown import update_markdown_document


def get_cas_from_files():
    """ Get CAS from action files. """
    fc = FileClient()
    files = fc.get_all_files()
    return CollectiveActions.read_from_files(files).sort()


def get_cas_from_csv():
    """ Get CAS from CSV. """
    df = pd.read_csv(CSV)
    return CollectiveActions.read_from_df(df).sort()


def get_cas_from_json():
    """ Get CAS from JSON. """
    df = pd.read_json(JSON)
    return CollectiveActions.read_from_df(df).sort()


def save_cas_to_readme(cas: CollectiveActions):
    """ Save CAS to README.md. """
    readme = Path(README)
    md_document = readme.read_text()
    md_document = update_markdown_document(
        md_document, CollectiveActions.ca_id, cas
    )
    readme.write_text(md_document)


def save_cas_to_csv(cas: CollectiveActions):
    """ Save CAS to CSV. """
    df = cas.to_df()
    df.to_csv(CSV)


def save_cas_to_json(cas: CollectiveActions):
    """ Save CAS to JSON. """
    data = cas.to_dict()
    with open(JSON, "w") as outfile:
        json.dump(data, outfile, default=ca_json_converter, indent=4)
