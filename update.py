import os
import textwrap
import argparse
import pandas as pd
import warnings
from pathlib import Path
from utils.collective_action import CollectiveAction, CollectiveActions
from utils.markdown import (
    update_markdown_document,
    SUMMARY_ID,
    MarkdownData,
    MarkdownDocument,
)
from utils.files import FileClient

README = Path(
    os.path.realpath(
        os.path.join(os.path.abspath(__file__), os.pardir, "README.md")
    )
)
CSV = Path(
    os.path.realpath(
        os.path.join(os.path.abspath(__file__), os.pardir, "actions.csv")
    )
)


def _get_parser():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
        This script is used to:
        - clean up files under /actions
        - export the actions to a csv
        - export the actions to the readme
		"""
        ),
        epilog=textwrap.dedent(
            """
        # Update files in action folder
        $ python update.py --files-cleanup

        # Update actions.csv based on files
        $ python update.py --files-to-csv

        # Update README.md based on files
        $ python update.py --files-to-readme
        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--files-cleanup",
        action="store_true",
        help="Update the collective action folder by cleaning it up and sorting it.",
    )
    parser.add_argument(
        "--files-to-csv",
        action="store_true",
        help="Update data.csv based on the action folder.",
    )
    parser.add_argument(
        "--files-to-readme",
        action="store_true",
        help="Update the table in the README.md based on the action folder.",
    )
    parser.add_argument(
        "--csv-cleanup",
        action="store_true",
        help="Update the csv file by cleaning it up and sorting it.",
    )
    parser.add_argument(
        "--csv-to-files",
        action="store_true",
        help="Update the collective action folder from the actions.csv.",
    )
    parser.add_argument(
        "--csv-to-readme",
        action="store_true",
        help="Update the table in the README.md from the actions.csv.",
    )

    args = parser.parse_args()
    return args


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


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning, module="bs4")
    args = _get_parser()

    if args.files_cleanup:
        print("Cleaning up actions in files...")
        cas = get_cas_from_files()
        cas.to_files()

    if args.files_to_csv:
        print("Using files to update the CSV...")
        cas = get_cas_from_files()
        save_cas_to_csv(cas)

    if args.files_to_readme:
        print("Using files to update the README...")
        cas = get_cas_from_files()
        save_cas_to_readme(cas)

    if args.csv_cleanup:
        print("Cleaning up the csv file...")
        cas = get_cas_from_csv()
        save_cas_to_csv(cas)

    if args.csv_to_files:
        print("Using csv to update the files...")
        cas = get_cas_from_csv()
        cas.to_files()

    if args.csv_to_readme:
        print("Using csv to update the README...")
        cas = get_cas_from_csv()
        save_cas_to_readme(cas)
