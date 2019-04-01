import os
import io
import re
import json
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

TOTAL_COLUMNS = 8
META_FIELD_PATTERN = "[meta]"
PROJECT_NAME = "collective-actions-in-tech"
HEADER_ROW_ID = "header"
MD_PATH = os.path.realpath(
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


def _serialize_meta_field(key: str) -> str:
    """ """
    return f"{META_FIELD_PATTERN}{key}"


def _deserialize_meta_field(key: str) -> str:
    """ """
    return key[len(META_FIELD_PATTERN) :]


def _md_table_to_df(table: MarkdownTable) -> pd.DataFrame:
    """ Converts a markdown table to a DataFrame. """
    assert _is_valid_table(table)
    actions = []
    soup = BeautifulSoup(table, "html.parser")
    trs = soup.table.find_all("tr")
    for i, tr in enumerate(trs):
        action = {}
        tds = tr.find_all("td")
        if ('id' not in tr.attrs) or ('id' in tr.attrs and tr.attrs['id'] != HEADER_ROW_ID):
            for key, val in tr.attrs.items():
                action[_serialize_meta_field(key)] = val
            for td in tds:
                key = td["data-column"]
                val = td.string.strip()
                action[key] = val
        if action:
            actions.append(action)
    return pd.read_json(json.dumps(actions), orient="list")


def _df_to_md_table(df: pd.DataFrame, table_id: str) -> MarkdownTable:
    """ Converts a DataFrame to a markdown table. """
    soup = BeautifulSoup(f"<table id={table_id}></table>", "html.parser")
    cols = df.columns

    # add row of headers
    tr = soup.new_tag("tr")
    tr['id'] = HEADER_ROW_ID
    soup.table.append(tr)
    for col in cols:
        if not col.startswith(META_FIELD_PATTERN):
            td = soup.new_tag("td")
            td.string = str(col)
            tr.append(td)

    # add actions
    for index, row in df.iterrows():
        tr = soup.new_tag("tr")
        soup.table.append(tr)
        for col in cols:
            if col.startswith(META_FIELD_PATTERN):
                tr[_deserialize_meta_field(col)] = row[col]
            else:
                td = soup.new_tag("td")
                td["data-column"] = col
                td.string = str(row[col])
                tr.append(td)

    return soup.prettify()


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


def _is_valid_table(table: MarkdownTable) -> bool:
    """ Checks if markdown table is malformed.

    Checks:
    - the number of td elements inside each tr element equals TOTAL_COLUMNS
    """
    assert table.startswith("<table")
    assert table.endswith("</table>")
    soup = BeautifulSoup(table, "html.parser")
    trs = soup.table.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) != TOTAL_COLUMNS:
            return False
    return True


def _clean_md_table(table: MarkdownTable) -> MarkdownTable:
    """ Cleans up the markdown table. """
    soup = BeautifulSoup(table, "html.parser")
    return soup.prettify()


def _replace_md_table(doc: MarkdownDocument, table_id: str, table: MarkdownTable) -> MarkdownDocument:
    """ Replace the table in {doc} with {table}. """
    assert _is_valid_table(table)
    new_table = BeautifulSoup(table, 'html.parser')
    soup = BeautifulSoup(doc, 'html.parser')
    table = soup.find("table", id=table_id)
    if not table:
        raise TableNotFound
    old_soup = table.replace_with(new_table)
    return soup.prettify()


def _sort_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Sort dataframe by date. 

    Date is not used as index as multiple actions may happen on one date.

    Args:
        df (pd.DataFrame): The dataframe to sort
    
    Returns:
        pd.Dataframe: the sorted Dataframe
    """
    if "date" not in df.columns:
        raise DateColumnNotFound
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values(by=["date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


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
    df = _md_table_to_df(table)
    df = _sort_df(df)
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
    df = _md_table_to_df(table)
    df = _sort_df(df)
    return df


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
    df = _md_table_to_df(table)
    df = _sort_df(df)
    table = _df_to_md_table(df, table_id)
    updated_md_document = _replace_md_table(md_document, table_id, table)
    input_fp.write_text(updated_md_document)
