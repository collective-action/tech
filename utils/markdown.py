import re
import datetime
import pytz
from copy import copy
from bs4 import BeautifulSoup

SUMMARY_ID = "summary"

MarkdownData = str
MarkdownDocument = str


class MarkdownDataNotFound(Exception):
    pass


class SummaryDataNotFound(Exception):
    pass


class MultipleMarkdownDataFound(Exception):
    pass


def replace_md_data(
    doc: MarkdownDocument, cas_id: str, md_data: MarkdownData
) -> MarkdownDocument:
    """ Replace the table in {doc} with {md_data}.

    Replace the old markdown data with new md data that is passed into this function.

    Args:
        doc: The markdown document to modify
        cas_id: The id of the md data div to look for
        md_data: The markdown data to replace the old one with

    Raises:
        MarkdownDataNotFound: if no such table is found
        MultipleMarkdownDataFound: if multiple tables are found

    Return:
        Updated markdown document
    """
    new_md_data = BeautifulSoup(md_data, "html.parser")
    old_md_data = re.findall(fr'<div id="{cas_id}">+[\s\S]+<\/div>', doc)
    if not old_md_data:
        raise MarkdownDataNotFound
    if len(old_md_data) > 1:
        raise MultipleMarkdownDataFound
    return doc.replace(old_md_data[0], new_md_data.prettify())


def update_ca_summary(
    doc: MarkdownDocument,
    summary_id: str,
    summary_field: str,
    summary_value: str,
) -> MarkdownDocument:
    """ Update a summary field in the markdown document. """
    soup = BeautifulSoup(doc, "html.parser")
    div = soup.find("div", id=summary_id)
    if not div:
        raise SummaryDataNotFound("<div> is missing.")
    td = div.table.find("td", {"data-summary": summary_field})
    if not td:
        raise SummaryDataNotFound(
            f"<td> with 'data-summary={summary_field}' is missing."
        )
    td_new = copy(td)
    td_new.string = summary_value
    return doc.replace(str(td), str(td_new))


def update_markdown_document(
    doc: MarkdownDocument,
    ca_id: str,
    cas: "CollectiveActions",
) -> MarkdownDocument:
    """ Replace markdown table and update summary. """
    doc = replace_md_data(
        doc, ca_id, cas.to_readme()
    )
    doc = update_ca_summary(
        doc, SUMMARY_ID, "action-count", str(len(actions))
    )
    tz = pytz.timezone("US/Eastern")
    now = datetime.datetime.now(tz).strftime("%d/%m/%Y %I:%M%p")
    doc = update_ca_summary(doc, SUMMARY_ID, "timestamp", now)
    return doc
