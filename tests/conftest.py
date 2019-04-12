import pytest


@pytest.fixture(scope="session")
def markdown():
    """ Return a markdown string for the tests to use. """
    return """
    <table data-author="name">
        <tr>
            <td class="field-key">data</td>
            <td class="field-value">2019-01-01</td>
        <tr>
    </table>
    """


@pytest.fixture(scope="session")
def df():
    """ Return a dataframe for the tests to use. """
    pass
