import datetime
from bs4 import BeautifulSoup
from utils.markdown import *


def test_replace_md_data():
    """ Tests the replace md data function. """
    start_text = "Some random text"
    actions_id = "test_action"
    doc = f"""{start_text}

<div id="{actions_id}">
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
    updated_actions_id = "updated"
    md_data = f"""
<div id="{updated_actions_id}">
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
    updated_doc = replace_md_data(doc, actions_id, md_data)
    assert updated_doc.startswith(start_text)
    md = re.findall(fr'<div id="{updated_actions_id}">+[\s\S]+<\/div>', updated_doc)
    soup = BeautifulSoup(md[0], "html.parser")
    assert soup.div.attrs["id"] == updated_actions_id


def test_update_summary_action():
    """ Tests the update summary function. """
    # TODO
    pass


def test_update_markdown_document():
    """ Tests the update markdown document function. """
    # TODO
    pass
