import os
import textwrap
import argparse
import pandas as pd
from pathlib import Path
from utils.action import Action, Actions
from utils.markdown import (
    update_markdown_document,
    SUMMARY_ID,
    MarkdownData,
    MarkdownDocument,
)
from utils.files import FileClient

README = Path(
    os.path.realpath(os.path.join(os.path.abspath(__file__), os.pardir, "README.md"))
)
CSV = Path(
    os.path.realpath(os.path.join(os.path.abspath(__file__), os.pardir, "actions.csv"))
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
        "--files-to-csv",
        action="store_true",
        help="Update data.csv based on the action folder."
    )
    parser.add_argument(
        "--files-to-readme",
        action="store_true",
        help="Update the table in the README.md based on the action folder."
    )
    parser.add_argument(
        "--files-cleanup",
        action="store_true",
        help="Update the action folder by cleaning it up and sorting it."
    )
    parser.add_argument(
        "--csv-to-files",
        action="store_true",
        help="Update the action folder from the actions.csv."
    )

    args = parser.parse_args()
    return args


def update_files_from_csv():
    print(f"Updating files in the /actions folder from actions.csv...")
    df = pd.read_csv(CSV)
    actions = Actions.read_from_df(df)
    actions.to_files()


def update_files():
    print(f"Updating files in the /actions folder...")
    fc = FileClient()
    files = fc.get_all_files()
    actions = Actions.read_from_files(files)
    actions.to_files()


def update_csv_from_files():
    print(f"Updating actions.csv from files in the /actions folder...")
    fc = FileClient()
    files = fc.get_all_files()
    actions = Actions.read_from_files(files)
    df = actions.to_df()
    df.to_csv(CSV)


def update_readme_from_files():
    print(f"Updating README.md from files in the /actions folder...")
    fc = FileClient()
    files = fc.get_all_files()
    actions = Actions.read_from_files(files)
    actions.sort()
    readme = Path(README)
    md_document = readme.read_text()
    md_document = update_markdown_document(md_document, Actions.action_id, actions)
    readme.write_text(md_document)


if __name__ == "__main__":
    args = _get_parser()
    if args.files:
        update_files()
    if args.files_to_csv:
        update_csv_from_files()
    if args.files_to_readme:
        update_readme_from_files()
    if args.csv_to_files:
        update_files_from_csv()
