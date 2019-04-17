import pytest
import pandas as pd
from utils.action import Action, Actions


@pytest.fixture(scope="session")
def correctly_formatted_md_action() -> str:
    """ Return a markdown string for of a single action. """
    return """
<table author="organizejs">
 <tr>
  <td class="field-key">date</td>
  <td class="field-value">2019-04-10</td>
 </tr>
 <tr>
  <td class="field-key">sources</td>
  <td class="field-value">
   <a
   href="https://www.recode.net/2019/4/10/18304877/amazon-climate-change-employees-tech-activism"
   target="_blank">www.recode.net</a>
  </td>
 </tr>
 <tr>
  <td class="field-key">action</td>
  <td class="field-value">open_letter</td>
 </tr>
 <tr>
  <td class="field-key">struggles</td>
  <td class="field-value">ethics</td>
 </tr>
 <tr>
  <td class="field-key">description</td>
  <td class="field-value">
   More than 3,500 of the company's corporate employees signed their names to a letter published on Wednesday that urged Jeff Bezos to create a comprehensive climate-change plan for the company.
  </td>
 </tr>
 <tr>
  <td class="field-key">locations</td>
  <td class="field-value">online</td>
 </tr>
 <tr>
  <td class="field-key">companies</td>
  <td class="field-value">amazon</td>
 </tr>
 <tr>
  <td class="field-key">workers</td>
  <td class="field-value">4000</td>
 </tr>
 <tr>
  <td class="field-key">tags</td>
  <td class="field-value">environmental</td>
 </tr>
</table>
"""


@pytest.fixture(scope="session")
def correctly_formatted_series_action() -> pd.Series:
    """ Return a markdown string for the tests to use. """
    return pd.Series(
        {
            "author": "organizejs",
            "date": "2019-04-10",
            "sources": "https://www.recode.net/2019/4/10/18304877/amazon-climate-change-employees-tech-activism",
            "action": "open_letter",
            "struggles": "ethics",
            "description": "More than 3,500 of the company's corporate employees signed their names to a letter published on Wednesday that urged Jeff Bezos to create a comprehensive climate-change plan for the company.",
            "locations": "online",
            "companies": "amazon",
            "workers": 4000,
            "tags": "environmental",
        }
    )


@pytest.fixture(scope="session")
def correctly_formatted_md_actions():
    """ Return a markdown string for the tests to use. """
    return """
<div id="actions">
 <table author="organizejs">
  <tr>
   <td class="field-key">date</td>
   <td class="field-value">2019-04-10</td>
  </tr>
  <tr>
   <td class="field-key">sources</td>
   <td class="field-value">
    <a
    href="https://www.recode.net/2019/4/10/18304877/amazon-climate-change-employees-tech-activism"
    target="_blank">www.recode.net</a>
   </td>
  </tr>
  <tr>
   <td class="field-key">action</td>
   <td class="field-value">open_letter</td>
  </tr>
  <tr>
   <td class="field-key">struggles</td>
   <td class="field-value">ethics</td>
  </tr>
  <tr>
   <td class="field-key">description</td>
   <td class="field-value">
    More than 3,500 of the company's corporate employees signed their names to a letter published on Wednesday that urged Jeff Bezos to create a comprehensive climate-change plan for the company.
   </td>
  </tr>
  <tr>
   <td class="field-key">locations</td>
   <td class="field-value">online</td>
  </tr>
  <tr>
   <td class="field-key">companies</td>
   <td class="field-value">amazon</td>
  </tr>
  <tr>
   <td class="field-key">workers</td>
   <td class="field-value">4000</td>
  </tr>
  <tr>
   <td class="field-key">tags</td>
   <td class="field-value">environmental</td>
  </tr>
 </table>
 <table author="organizejs">
  <tr>
   <td class="field-key">date</td>
   <td class="field-value">2019-04-04</td>
  </tr>
  <tr>
   <td class="field-key">sources</td>
   <td class="field-value">
    <a href="https://www.wired.com/story/microsoft-employees-protest-treatment-women-ceo-nadella/" target="_blank">www.wired.com</a>
   </td>
  </tr>
  <tr>
   <td class="field-key">action</td>
   <td class="field-value">protest</td>
  </tr>
  <tr>
   <td class="field-key">struggles</td>
   <td class="field-value">discrimination</td>
  </tr>
  <tr>
   <td class="field-key">description</td>
   <td class="field-value">
    A group of Microsoft employees appeared at an employee meeting with CEO Satya Nadella Thursday to protest the companies's treatment of women. It's not clear how many were part of the protest, but some female and male employees at the event wore all white, inspired by the congresswomen who wore suffragette white to the State of the Union in February.
   </td>
  </tr>
  <tr>
   <td class="field-key">locations</td>
   <td class="field-value">seattle</td>
  </tr>
  <tr>
   <td class="field-key">companies</td>
   <td class="field-value">microsoft</td>
  </tr>
 </table>
 <table author="organizejs">
  <tr>
   <td class="field-key">date</td>
   <td class="field-value">2019-04-02</td>
  </tr>
  <tr>
   <td class="field-key">sources</td>
   <td class="field-value">
    <a
    href="https://www.theguardian.com/technology/2019/apr/02/google-workers-sign-letter-temp-contractors-protest"
    target="_blank">www.theguardian.com</a>
   </td>
  </tr>
  <tr>
   <td class="field-key">action</td>
   <td class="field-value">open_letter</td>
  </tr>
  <tr>
   <td class="field-key">struggles</td>
   <td class="field-value">working_conditions, pay_and_benefits</td>
  </tr>
  <tr>
   <td class="field-key">description</td>
   <td class="field-value">
    More than 900 Google workers have signed a letter objecting to the tech giant's treatment of temporary contractors, in what organizers are calling a 'historical coalition' between Google's full-time employees (FTEs) and temps, vendors and contractors (TVCs).
   </td>
  </tr>
  <tr>
   <td class="field-key">locations</td>
   <td class="field-value">online</td>
  </tr>
  <tr>
   <td class="field-key">companies</td>
   <td class="field-value">google</td>
  </tr>
  <tr>
   <td class="field-key">workers</td>
   <td class="field-value">900</td>
  </tr>
 </table>
</div>
"""


@pytest.fixture(scope="session")
def correctly_formatted_df_actions():
    """ Return a dataframe for the tests to use. """
    return pd.DataFrame(
        [
            {
                "author": "organizejs",
                "date": "2019-04-10",
                "sources": "https://www.recode.net/2019/4/10/18304877/amazon-climate-change-employees-tech-activism",
                "action": "open_letter",
                "struggles": "ethics",
                "description": "More than 3,500 of the company's corporate employees signed their names to a letter published on Wednesday that urged Jeff Bezos to create a comprehensive climate-change plan for the company.",
                "locations": "online",
                "companies": "amazon",
                "workers": 4000,
                "tags": "environmental",
            },
            {
                "author": "organizejs",
                "date": "2019-04-04",
                "sources": "https://www.wired.com/story/microsoft-employees-protest-treatment-women-ceo-nadella/",
                "action": "protest",
                "struggles": "discrimination",
                "description": "A group of Microsoft employees appeared at an employee meeting with CEO Satya Nadella Thursday to protest the companies's treatment of women. It's not clear how many were part of the protest, but some female and male employees at the event wore all white, inspired by the congresswomen who wore suffragette white to the State of the Union in February.",
                "locations": "seattle",
                "companies": "microsoft",
            },
            {
                "author": "organizejs",
                "date": "2019-04-02",
                "sources": "https://www.theguardian.com/technology/2019/apr/02/google-workers-sign-letter-temp-contractors-protest",
                "action": "open_letter",
                "struggles": ["working_conditions", "pay_and_benefits"],
                "description": "More than 900 Google workers have signed a letter objecting to the tech giant's treatment of temporary contractors, in what organizers are calling a 'historical coalition' between Google's full-time employees (FTEs) and temps, vendors and contractors (TVCs).",
                "locations": "online",
                "companies": "google",
                "workers": 900,
            },
        ]
    )

