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
        # Convert to CSV file
        $ python convert.py --to-csv --output data.csv

        # Clean up the table in the README file
        $ python convert.py --update-readme

        # Updates the table in the README file using a csv file
        $ python convert.py --update-readme --csv data.csv
        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--to-csv",
        action="store_true",
        help="Converts the table in the README to a csv file.",
    )
    parser.add_argument("--output", help="Name of the output csv.")

    parser.add_argument(
        "--update-readme", action="store_true", help="Update the table in the README."
    )
    parser.add_argument("--csv", help="uses csv to update readme")

    args = parser.parse_args()
    if args.to_csv and (args.output is None):
        parser.error("--to-csv requires --output.")
    if args.csv and (args.update_readme is None):
        parser.error("--csv requires --update-readme.")
    return args


def clean_readme(input_fp: Path, output_fp: Path):
    md_document = input_fp.read_text()
    actions = Actions.read_from_md(md_document)
    actions.sort(reverse=True)
    md_document = update_markdown_document(md_document, Actions.action_id, actions)
    output_fp.write_text(md_document)


def save_readme_to_csv(input_fp: Path, output_fp: Path):
    md_document = input_fp.read_text()
    actions = Actions.read_from_md(md_document)
    actions.sort(reverse=True)
    df = actions.to_df()
    df.to_csv(output_fp)


def update_readme_with_csv(readme: Path, csv: Path):
    md_document = readme.read_text()
    df = pd.read_csv(csv)
    actions = Actions.read_from_df(df)
    actions.sort(reverse=True)
    md_document = update_markdown_document(md_document, Actions.action_id, actions)
    readme.write_text(md_document)


if __name__ == "__main__":
    args = _get_parser()
    if args.update_readme:
        output_fp = Path(args.output) if args.output else README_PATH
        clean_readme(README_PATH, output_fp)
    if args.update_readme and args.csv:
        update_readme_with_csv(README_PATH, Path(args.csv))
    if args.to_csv:
        save_readme_to_csv(README_PATH, Path(args.output))
