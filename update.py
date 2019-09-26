import os
import textwrap
import argparse
import warnings
from utils.files import FileClient
from utils.convert import (
    get_cas_from_csv,
    get_cas_from_files,
    save_cas_to_readme,
    save_cas_to_csv,
    README,
    CSV
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
        help="automatically detect if csv of files are most up-to-date and update accordingly."
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


def was_csv_updated() -> bool:
    """ This function compares the last modified time on the csv file to the
    actions folder to check which was last modified. """
    csv_last_modified_time = os.path.getmtime(str(CSV))
    files_last_modified_time = os.path.getmtime(str(FileClient.get_cas_folder()))
    return (
        True
        if csv_last_modified_time > files_last_modified_time
        else False
    )


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning, module="bs4")
    args = _get_parser()

    if args.auto:
        print("Update repo automatically.")
        if was_csv_updated():
            print("CSV is most up-to-date, updating files and readme accordingly.")
            cas = get_cas_from_csv()
            save_cas_to_csv(cas)
            cas.to_files()
        else:
            print("Files are most up-to-date, updating csv and readme accordingly.")
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
