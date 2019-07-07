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

README_PATH = Path(
    os.path.realpath(os.path.join(os.path.abspath(__file__), os.pardir, "README.md"))
)


def _get_parser():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
        This script is used to:
        - clean up the passed in markdown file,
        - export the table in the passed in markdown file to a csv
		"""
        ),
        epilog=textwrap.dedent(
            """
        # Update files in action folder
        $ python update.py --files

        # Update actions.csv based on files
        $ python update.py --to-csv

        # Update README.md based on files
        $ python update.py --to-readme
        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--to-csv",
        action="store_true",
        help="Update data.csv based on the action folder."
    )
    parser.add_argument(
        "--to-readme",
        action="store_true",
        help="Update the table in the README.md based on the action folder."
    )
    parser.add_argument(
        "--files",
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
    df = pd.read_csv("actions.csv")
    actions = Actions.read_from_df(df)
    actions.sort()
    actions.to_files()


def update_files():
    print(f"Updating files in the /actions folder...")
    fc = FileClient()
    files = fc.get_all_files()
    actions = Actions.read_from_files(files)
    actions.sort()
    actions.to_files()


def update_csv_from_files():
    print(f"Updating actions.csv from files in the /actions folder...")
    fc = FileClient()
    files = fc.get_all_files()
    actions = Actions.read_from_files(files)
    actions.sort()
    df = actions.to_df()
    df.to_csv("actions.csv")


def update_readme_from_files():
    print(f"Updating README.md from files in the /actions folder...")
    fc = FileClient()
    files = fc.get_all_files()
    actions = Actions.read_from_files(files)
    actions.sort(reverse=True)
    readme = Path("README.md")
    md_document = readme.read_text()
    md_document = update_markdown_document(md_document, Actions.action_id, actions)
    readme.write_text(md_document)


if __name__ == "__main__":
    args = _get_parser()
    if args.files:
        update_files()
    if args.to_csv:
        update_csv_from_files()
    if args.to_readme:
        update_readme_from_files()
    if args.csv_to_files:
        update_files_from_csv()
