# Contribution Guidelines

One of the goals of this repo is to make sure that the data is as update-to-date as possible, so please feel free to make additions to the dataset as current events unfold!

To contribute, please use pull requests to add to the repo so that new additions can be checked for formatting, accuracy and validity.

This document will cover how to make a contribute:
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
1. Make a [pull request](https://help.github.com/en/articles/creating-a-pull-request) from the branch you've created into the master branch.

## Data Fields

When adding a new action, collect data on the following fields. If one or more
of the fields are not applicable, you can omit the field. However, you cannot
add a new field at this time. If there is additional information you'd like to
include, add it in the description field.

> Take note of the plurality of the fields. `action` is singular while `sources` is plural. 

| Field | Required | Description |
| --- | --- | --- |
| date | True | While the date may seem trivial, collecting dates may be comlex for multi-day events such as pickets or online petitions. In this repo, we collect only the start date of the action in the format YYYY-MM-DD. |
| sources | True | The url(s) of reliable sources that has reported on this event. |
| action | True | What was the form of the action that took place? (`union_drive`, `union_representation`, `open_letter`, `strike`, `protest`)|
| struggles | True | The kind of struggle workers are standing up against. (`pay_and_benefits`, `working_conditions`, `unfair_labor_practices`, `job_security`, `ethics`, `discrimination`)| 
| description | True | A short sentence describing the event where you can include information that isn't covered in the fields above. |
| locations | False | The location(s) of the action, or whether it was online. |
| companies | False | Which company are workers are standing up against? Some moments of worker power may not have an associated company. For example, online petitions or a protests against the president may consist of workers from an amalgamation of companies. In which case we can omit this field. |
| workers | False | The number of workers active in the action. Since we're only looking at collective actions, the number must be more than 1. Sometimes the sources do not state a concrete number when reporting. In those cases, lean on the conservative side. For example: "Hundreds of Uber drivers..." --> 100 |
| tags | False | Tag the event with a term or word that you feel is relevant but not captured by the other fields. |

In the table above, `action` and `struggles` must contain only the following values:

| Fields | Valid Values | 
| --- | --- |
| action | strike, protest, open_letter, legal_action, union_drive, union_represenation | 
| struggles | ethics, pay_and_benefits, working_conditions, discrimination, unfair_labor_practices, job_security |

## Formatting
When adding an update to the README, use the provided html code below to add a
action. Copy and paste the html snippet under the opening `<div>` tag in the README.

```html
<!-- Example only -->
 <table author="organizejs">
  <tr>
   <td class="field-key">date</td>
   <td class="field-value">2018-01-01</td>
  </tr>
  <tr>
   <td class="field-key">sources</td>
   <td class="field-value">
    <a href="https://www.your.valid/source">CNN</a>,
    <a href="https://www.your.valid/source">BBC</a>,
   </td>
  </tr>
  <tr>
   <td class="field-key">companies</td>
   <td class="field-value">Amazon</td>
  </tr>
  <tr>
   <td class="field-key">action</td>
   <td class="field-value">protest</td>
  </tr>
  <tr>
   <td class="field-key">struggles</td>
   <td class="field-value">ethics</td>
  </tr>
  <tr>
   <td class="field-key">worker</td>
   <td class="field-value">1000</td>
  </tr>
  <tr>
   <td class="field-key">description</td>
   <td class="field-value">Thousands of people protest a military contract in Queens.</td>
  </tr>
  <tr>
   <td class="field-key">locations</td>
   <td class="field-value">New York</td>
  </tr>
  <tr>
   <td class="field-key">tags</td>
   <td class="field-value">non_tech_centric</td>
  </tr>
 </table>
```

Please note the following aspects:
- If you would like your github username affiliated with the action you added,
  add an attribute `author` in the `<table>` tag with your github username.
  If you wish to remain anonymous, skip this step. Keep in mind, your github
  username will be affiliated with the PR.
- Each `<td>` tag must have either have the class `field-key` or `field-value`.
- If you add multiple values to a field, make sure the values are
  comma-seprated. For example, if two types of struggle were involved in the action,
  it would look like so: `pay_and_benefits, working_conditions`
- If a field is not applicable, remove the `<tr>` tag for it entirely.
- DO NOT add additional fields to the table. If you wish to include other
  information, add it in the description field or as a tag.

## Making A Pull Request (PR)

You can learn about how to make a pull request [here](https://help.github.com/en/articles/creating-a-pull-request). 

When you make a pull request, the request will trigger an Azure pipeline to kick off where it will perform the following:
1. Test that the addition that was made complies with the data fields outlined above - if it does not comply, the Azure pipeline will block the merge.
1. Cleans up the HTML code and updates the summary, including how many actions are reported
1. Generates/updates the `actions.csv` file so that the file is up-to-date

> The cleanup/update uses the `convert.py` file described in the "Developer Feature" section below

After the azure pipeline performs these steps, it will automatically add the changes to the PR.

## Developer Features

This repository comes with a `convert.py` located in the root directory. You can
use this file to clean up the table (such as sorting the contents of the table by
date) and save the data to a csv.

```sh
# to save to csv
python convert.py --to-csv --output <output_file_path>

# to sort the actions in the readme and update the summary
python convert.py --update-readme

# to update the readme using an updated csv file
python convert.py --update-readme --csv new_actions.csv
```
