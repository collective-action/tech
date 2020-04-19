import re
from bs4 import BeautifulSoup
from utils.markdown import replace_md_data


def test_replace_md_data():
    """ Tests the replace md data function. """
    start_text = "Some random text"
    cas_id = "test_action"
    doc = f"""{start_text}

<div id="{cas_id}">
    <table>
        <tr>
            <td>foo</td><td>bar</td>
        </tr>
        <tr>
            <td>foo</td><td>bar</td>
        </tr>
    </table>
</div>
"""
    updated_cas_id = "updated"
    md_data = f"""
<div id="{updated_cas_id}">
    <table>
        <tr>
            <td>foo</td><td>bar</td>
        </tr>
        <tr>
            <td>foo</td><td>bar</td>
        </tr>
    </table>
</div>
"""
    updated_doc = replace_md_data(doc, cas_id, md_data)
    assert updated_doc.startswith(start_text)
    md = re.findall(
        fr'<div id="{updated_cas_id}">+[\s\S]+<\/div>', updated_doc
    )
    soup = BeautifulSoup(md[0], "html.parser")
    assert soup.div.attrs["id"] == updated_cas_id


def test_update_summary_action():
    """ Tests the update summary function. """
    # TODO
    pass


def test_update_markdown_document():
    """ Tests the update markdown document function. """
    # TODO
    pass
