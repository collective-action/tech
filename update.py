import os
import textwrap
import argparse
import warnings
from utils.convert import (
    get_cas_from_csv,
    get_cas_from_files,
    save_cas_to_readme,
    save_cas_to_csv,
    save_cas_to_json,
    README,
    CSV,
    CSV_FLAG,
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
        # Automatically detect if csv or files are most up-to-date and update
        # accordingly
        $ python update.py --auto

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
        "--auto",
        action="store_true",
        help="automatically detect if csv of files are most up-to-date and update accordingly.",
    )
    parser.add_argument(
        "--files-cleanup",
        action="store_true",
        help="Update the collective action folder by cleaning it up and sorting it.",
    )
    parser.add_argument(
        "--files-to-csv",
        action="store_true",
        help="Update actions.csv based on the action folder.",
    )
    parser.add_argument(
        "--files-to-json",
        action="store_true",
        help="Update actions.json based on the action folder.",
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


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning, module="bs4")
    args = _get_parser()

    if args.auto:
        print("Update repo automatically.")
        if CSV_FLAG.exists():
            print(
                "CSV_FLAG is present; updating files and readme accordingly."
            )
            cas = get_cas_from_csv()
            save_cas_to_csv(cas)
            cas.to_files()
            os.remove(CSV_FLAG)
        else:
            print(
                "CSV_FLAG is not present; updating csv and readme accordingly."
            )
            cas = get_cas_from_files()
            cas.to_files()
            save_cas_to_csv(cas)
        save_cas_to_readme(cas)

    if args.files_cleanup:
        print("Cleaning up actions in files...")
        cas = get_cas_from_files()
        cas.to_files()

    if args.files_to_csv:
        print("Using files to update the CSV...")
        cas = get_cas_from_files()
        save_cas_to_csv(cas)

    if args.files_to_json:
        print("Using files to update the JSON...")
        cas = get_cas_from_files()
        save_cas_to_json(cas)

    if args.files_to_readme:
        print("Using files to update the README...")
        cas = get_cas_from_files()
        save_cas_to_readme(cas)

    if args.csv_cleanup:
        print("Cleaning up the csv file...")
        cas = get_cas_from_csv()
        save_cas_to_csv(cas)

    if args.csv_to_files:
        print("Clearning up the actions in the csv...")
        actions = get_cas_from_csv()
        save_actions_to_csv(actions)

    if args.csv_to_files:
        print("Using csv to update the files...")
        cas = get_cas_from_csv()
        cas.to_files()

    if args.csv_to_readme:
        print("Using csv to update the README...")
        cas = get_cas_from_csv()
        save_cas_to_readme(cas)
