import os
import json
import pandas as pd
from pathlib import Path

from utils.collective_action import CollectiveAction, CollectiveActions
from utils.files import FileClient
from utils.misc import ca_json_converter
from utils.markdown import update_markdown_document


README = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, os.pardir, "README.md"
        )
    )
)
CSV = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, os.pardir, "actions.csv"
        )
    )
)
JSON = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, os.pardir, "actions.json"
        )
    )
)
CSV_FLAG = Path(
    os.path.realpath(
        os.path.join(
            os.path.abspath(__file__), os.pardir, os.pardir, "CSV_FLAG"
        )
    )
)


def get_cas_from_files():
    fc = FileClient()
    files = fc.get_all_files()
    return CollectiveActions.read_from_files(files).sort()


def get_cas_from_csv():
    df = pd.read_csv(CSV)
    return CollectiveActions.read_from_df(df).sort()


def save_cas_to_readme(cas: CollectiveActions):
    readme = Path(README)
    md_document = readme.read_text()
    md_document = update_markdown_document(
        md_document, CollectiveActions.ca_id, cas
    )
    readme.write_text(md_document)


def save_cas_to_csv(cas: CollectiveActions):
    df = cas.to_df()
    df.to_csv(CSV)


def save_cas_to_json(cas: CollectiveActions):
    data = cas.to_dict()
    with open('actions.json', 'w') as outfile:
        json.dump(data, outfile, default=ca_json_converter)
