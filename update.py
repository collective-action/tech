import os
import textwrap
import argparse
import warnings
from utils.convert import (
    get_cas_from_csv,
    get_cas_from_json,
    get_cas_from_files,
    save_cas_to_readme,
    save_cas_to_csv,
    save_cas_to_json,
    save_cas_to_files,
)
from utils.misc import CSV_FLAG


def save_cas_to_all(cas: CollectiveActions):
    """ update cas to json, csv, readme, and actions folder. """
    save_cas_to_csv(cas)
    save_cas_to_json(cas)
    save_cas_to_readme(cas)
    cas.to_files()    

    
def _get_parser():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
        This script is used to:
        - clean up files under /actions
        - export the actions to a csv
        - export the actions to a json
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

        # Update actions.json based on files
        $ python update.py --files-to-json

        ...

        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="automatically detect if csv of files are most up-to-date and update accordingly.",
    )

    # files > Any
    parser.add_argument(
        "--files-cleanup",
        action="store_true",
        help="Update FOLDER by cleaning it up and sorting it.",
    )
    parser.add_argument(
        "--files-to-csv",
        action="store_true",
        help="Update CSV from action FOLDER.",
    )
    parser.add_argument(
        "--files-to-json",
        action="store_true",
        help="Update JSON from action FOLDER.",
    )
    parser.add_argument(
        "--files-to-readme",
        action="store_true",
        help="Update README.md from action FOLDER.",
    )

    # csv > Any
    parser.add_argument(
        "--csv-cleanup",
        action="store_true",
        help="Update CSV by cleaning it up and sorting it.",
    )
    parser.add_argument(
        "--csv-to-files",
        action="store_true",
        help="Update FOLDER from CSV file.",
    )
    parser.add_argument(
        "--csv-to-readme",
        action="store_true",
        help="Update README.md from CSV file.",
    )
    parser.add_argument(
        "--csv-to-json", action="store_true", help="Update JSON from CSV file."
    )

    # json > Any
    parser.add_argument(
        "--json-cleanup",
        action="store_true",
        help="Update JSON by cleaning it up and sorting it.",
    )
    parser.add_argument(
        "--json-to-files",
        action="store_true",
        help="Update FOLDER from JSON file.",
    )
    parser.add_argument(
        "--json-to-readme",
        action="store_true",
        help="Update README.md from JSON file.",
    )
    parser.add_argument(
        "--json-to-csv", action="store_true", help="Update CSV from JSON file."
    )

    args = parser.parse_args()
    return args
    

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning, module="bs4")
    args = _get_parser()

    # auto
    if args.auto:
        print("Update repo automatically.")
        if CSV_FLAG.exists():
            print(
                "CSV_FLAG is present; updating files, json and readme accordingly."
            )
            cas = get_cas_from_csv()
            os.remove(CSV_FLAG)
        else:
            print(
                "CSV_FLAG is not present; updating csv, json and readme using the action folder."
            )
            cas = get_cas_from_files()
        save_cas_to_all(cas)

    # files > Any
    if args.files_cleanup:
        print("Cleaning up actions folder...")
        cas = get_cas_from_files()
        save_cas_to_files(cas)

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

    # csv > Any
    if args.csv_cleanup:
        print("Cleaning up the CSV file...")
        cas = get_cas_from_csv()
        save_cas_to_csv(cas)

    if args.csv_to_files:
        print("Using CSV to update the action folder...")
        cas = get_cas_from_csv()
        save_cas_to_files(cas)

    if args.csv_to_readme:
        print("Using CSV to update the README...")
        cas = get_cas_from_csv()
        save_cas_to_readme(cas)

    if args.csv_to_json:
        print("Using CSV to update JSON...")
        cas = get_cas_from_csv()
        save_cas_to_json(cas)

    # json > Any
    if args.json_cleanup:
        print("Cleaning up the JSON file...")
        cas = get_cas_from_json()
        save_cas_to_json(cas)

    if args.json_to_files:
        print("Using JSON to update the action folder...")
        cas = get_cas_from_json()
        save_cas_to_files(cas)

    if args.json_to_readme:
        print("Using JSON to update README...")
        cas = get_cas_from_json()
        save_cas_to_readme(cas)

    if args.json_to_csv:
        print("Using JSON to update CSV...")
        cas = get_cas_from_json()
        save_cas_to_csv(cas)
