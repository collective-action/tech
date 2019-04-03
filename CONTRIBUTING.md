# Contribution Guidelines

One of the goals of this repo is to make sure that the data is as update-to-date as possible, so please feel free to make additions to the dataset as current events unfold!

To contribute, please use pull requests to add to the repo so that new additions can be checked for formatting, accuracy and validity.

This document will cover three aspects of making contributions:
1. Github steps
1. Data Fields
1. Formatting Guidelines
1. Developer Features

## Github Steps to Contributing
Here are the basic steps to adding a new action using a pull request:
1. Edit the README.md in Github.com
1. The master branch is protected, so you won't be able to merge directly into
   it. Instead, create a new branch (with the event name you want to add in
   the branch title), and open a pull-request.
1. Make a pull request from the branch you've created into the master branch.

## Data Fields

When adding a new action, collect data on the following fields. If one or more
of the fields are not applicable, you can omit the field. However, you cannot
add a new field at this time. If there is additional information you'd like to
include, add it in the description field.

| Field | Description |
| --- | --- |
| date | While the date may seem trivial, collecting dates may be comlex for multi-day events such as pickets or online petitions. In this repo, we collect only the start date of the action in the format YYYY-MM-DD. |
| company | Which is the company workers are standing up against? Some moments of worker power may not have an associated company. For example, online petitions or a protests against the president may consist of workers from an amalgamation of companies. In which case we can leave this field blank. |
| action | What was the form of the action that took place? |
| employment_type | What was the employment type of the workers who took action? FTEs? Contract workers? If there are multipe employment types, they should be listed in the order of most-relevant to least relevant. It is also possible that there is no affiliated employment type, which can be the case for many public petitions. |
| union_affiliation | Was a union affiliated? And if so, which one? |
| worker_count | The number of workers active in the action. Since we're only looking at collective actions, the number must be more than 1. Sometimes the sources do not state a concrete number when reporting. In those cases, lean on the conservative side. For example: "Hundreds of Uber drivers..." --> 100+ |
| struggle | The topic of struggle that caused the action. |
| source | The url of a reliable source that has reported on this event. |

## Formatting
When adding an update to the README, use the provided html code below to add a
row to the table.

```html
<!-- Example only -->
<table data-author="organizejs">
    <tr>
        <td class="field-key">date</td>
        <td class="field-value">2019-03-25</td>
    </tr>
    <tr>
        <td class="field-key">source</td>
        <td class="field-value">
            <a href="https://www.vox.com/2019/3/25/18280718/uber-lyft-drivers-strike-la-los-angeles">Vox</a>
        </td>
    </tr>
    <tr>
        <td class="field-key">company</td>
        <td class="field-value">Uber, Lyft</td>
    </tr>
    <tr>
        <td class="field-key">action</td>
        <td class="field-value">Strike</td>
    </tr>
    <tr>
        <td class="field-key">employment_type</td>
        <td class="field-value">Independent Contractors</td>
    </tr>
    <tr>
        <td class="field-key">worker_count</td>
        <td class="field-value">100+</td>
    </tr>
    <tr>
        <td class="field-key">struggle_type</td>
        <td class="field-value">Wages</td>
    </tr>
    <tr>
        <td class="field-key">description</td>
        <td class="field-value">Uber drivers stage 1-day strike in LA over cut reduction, Lyft drivers join</td>
    </tr>
</table>
```
When adding an action, use this html template, and insert it at the end of the `<table>` tag.

Please note the following aspects:
- If you would like your github username affiliated with the action you added,
  add an attribute `data-author` in the `<table>` tag with your github username.
  If you wish to remain anonymous, skip this step. Keep in mind, your github
  username will be affiliated with the PR.
- Each `<td>` tag must have either have the class `field-key` or `field-value`.
- Feel free to add multiple sources if it is relevant. Use the format
  `[publisher](url)` for it to render correctly.
- If you add multiple values to a field, make sure the values are
  comma-seprated. For example, if two types of struggle were involved in the action,
  it would look like so: `Wages, Health Benefits`
- If a field is not applicable, remove the `<tr>` tag for it entirely.
- DO NOT add additional fields to the table. If you wish to include other
  information, add it in the description field.

## Developer Features

This repository comes with a `convert.py` located in the root directory. You can
use this file to clean up the table (such as sorting the contents of the table by
date) and save the data to a csv.

```sh
# to save to csv
python convert.py --to-csv --output <output_file_path>

# to clean up the README
python convert.py --clean-doc
```

You can also use it in a notebook or in your python code.

```python
from utils.markdown import *

df = get_df_from_md_document(Path(MD_PATH))
```
