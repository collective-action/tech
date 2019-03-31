import os
import io
import re
import pandas as pd
from pathlib import Path
from IPython.display import Markdown, display

TOTAL_COLUMNS = 8

readme_path = os.path.realpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "README.md")
)

MarkdownTable = str
MarkdownDocument = str


class TableIDNotFound(Exception):
    pass


class DateColumnNotFound(Exception):
    pass


class TableNotFound(Exception):
    pass


class MultipleTablesFound(Exception):
    pass


class TableIsMalformed(Exception):
    pass


def _md_table_to_df(md: MarkdownTable) -> pd.DataFrame:
    """ Converts a markdown table to a DataFrame. """
    return pd.read_html(md, header=0)[0]


def _df_to_md_table(df: pd.DataFrame, table_id: str) -> MarkdownTable:
    """ Converts a DataFrame to a markdown table. """
    str_io = io.StringIO()
    df.to_html(buf=str_io, table_id=table_id, index=False)
    return str_io.getvalue()


def _get_table_from_md_document(table_id: str, doc: MarkdownDocument) -> MarkdownTable:
    """ Extract table from a markdown document.

	A markdown document may have multiple tables in it. This function will not
	extract any table from the document. Instead, it looks specifically for a
	table expressed in html with the id {table_id}.

	If multiple such tables are found, or none are found at all, it will raise
	an error.

	Args:
		table_id (str): the id of the table
		doc (MarkdownDocument): the markdown document to parse

	Raise:
		TableNotFound: if no such table is found
		MultipleTablesFound: if multiple tables are found
		TableIsMalformed: if table is malformed

	Returns:
		The parsed Markdown table
	"""
    tables = re.findall(fr"<table[\s\S]+{table_id}+[\s\S]+<\/table>", doc)
    if not tables:
        raise TableNotFound
    if len(tables) > 1:
        raise MultipleTablesFound
    assert len(tables) == 1
    table = tables[0]
    table = _clean_md_table(table)
    if not _is_valid_table(table):
        raise TableIsMalformed
    return table


def _md_to_csv(table: MarkdownTable, output_fp: Path) -> Path:
    """ Extracts a table from a markdown document to save as a csv.

	Parse {input_fp}, a path to a markdown document, for a table with the
	specified {table_id} and save the table as a csv file located at {output_fp}.

	Args:
		input_fp (Path): path to the markdown document to parse
		table_id (str): the id to use when parsing for the table
		output_fp (Path): the path to save the output csv to

	Rturns:
		(Path): The output csv path.
	"""
    pass
    # md = open(readme_path, "r")


def _is_valid_table(table: MarkdownTable) -> bool:
    """ Checks if markdown table is malformed.

	Checks:
	- the same number of td elements inside each tr element
	"""
    assert table.startswith("<table")
    assert table.endswith("</table>")
    trs = re.findall(fr"<tr[^>]*>(.*?)<\/tr>", table)
    for tr in trs:
        tds = re.findall(fr"<td[^>]*>(.*?)<\/td>", tr)
        if len(tds) != TOTAL_COLUMNS:
            return False
    return True


def _clean_md_table(table: MarkdownTable) -> MarkdownTable:
    """ Cleans up the markdown table. """
    table = re.sub(" +", " ", table)
    table = re.sub("\n", "", table)
    table = re.sub("> <", "><", table)
    return table


def _replace_md_table(doc: MarkdownDocument, table: MarkdownTable) -> MarkdownDocument:
    """ Replace the table in {doc} with {table}. """
    pass


def _sort_md_table(table: MarkdownTable) -> MarkdownTable:
    """ Sorts table. """
    assert _is_valid_table(table)
    df = _md_table_to_df(table)
    if 'date' not in df.columns:
        raise DateColumnNotFound
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=["date"], inplace=True)
    table_id = _get_md_table_id(table)
    return _df_to_md_table(df, table_id)


def _get_md_table_id(table: MarkdownTable) -> str:
    """ Extract the table id. """
    table_id = re.findall(fr"id=\"(.*?)\"", table)
    if not table_id:
        raise TableIDNotFound


def save_md_table_to_csv(input_fp: Path, table_id: str, output_fp: Path):
    """ Saves table in markdown document as csv.

	Saves a cleaned-up version of the table found in the passed in markdown
	file as a csv.

	Args:
		input_fp (Path): input file path
		table_id (str): the id of the element to search for when finding the
		table
		output_fp (Path): the output file path
	"""
    md_document = input_fp.read_text()
    table = _get_table_from_md_document(table_id, md_document)
    table = _sort_md_table(table)
    df = _md_table_to_df(table)
    df.to_csv(output_fp)


def get_df_from_md_document(input_fp: Path, table_id: str) -> pd.DataFrame:
    """ Gets df from table in markdown document.

	Returns a cleaned-up version of the table found in the passed in markdown
	file as a dataframe.

	Args:
		input_fp (Path): input file path
		table_id (str): the id of the element to search for when finding the
		table
	"""
    md_document = input_fp.read_text()
    table = _get_table_from_md_document(table_id, md_document)
    table = _sort_md_table(table)
    return _md_table_to_df(table)


def clean_md_document(input_fp: Path, table_id: str):
    """ Cleans the table from the markdown document.

	Replaces the table in the passed in markdown file with a cleaned-up version
	of the table.

	Args:
		input_fp (Path): input file path
		table_id (str): the id of the element to search for when finding the
		table
	"""
    md_document = input_fp.read_text()
    table = _get_table_from_md_document(table_id, md_document)
    table = _sort_md_table(table)
    updated_md_document = _replace_md_table(md_document, table)
    input_fp.write_text(updated_md_document)
