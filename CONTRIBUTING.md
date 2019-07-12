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
1. Create a new event under the '/actions' folder in the root directory on Github.com.
1. Create a new branch (with the event name you want to add in the branch title), and open a pull-request.
1. Make a [pull request](https://help.github.com/en/articles/creating-a-pull-request) from the branch you've created into the master branch.

## Data Fields

When adding a new action, collect data on the following fields. If one or more
of the fields are not applicable, you can omit the field. However, you cannot
add a new field at this time. If there is additional information you'd like to
include, add it in the description field.

> Take note of the plurality of the fields. `action` is singular while `sources` is plural. 

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| date | True | YYYY-MM-DD | While the date may seem trivial, collecting dates may be comlex for multi-day events such as pickets or online petitions. In this repo, we collect only the start date of the action in the format YYYY-MM-DD. |
| sources | True | List(url) | The url(s) of reliable sources that has reported on this event. |
| action | True | str | What was the form of the action that took place? (`union_drive`, `union_representation`, `open_letter`, `strike`, `protest`, `legal_action`)|
| struggles | True | List(str) | The kind of struggle workers are standing up against. (`pay_and_benefits`, `working_conditions`, `unfair_labor_practices`, `job_security`, `ethics`, `discrimination`)| 
| description | True | str | A short paragraph describing the event where you can include information that isn't covered in the fields above. Multiple paragraphs are not allowed in this field. |
| locations | False | List(str) | The location(s) of the action, or whether it was online. |
| companies | False | List(str) | Which company are workers are standing up against? Some moments of worker power may not have an associated company. For example, online petitions or a protests against the president may consist of workers from an amalgamation of companies. In which case we can omit this field. |
| workers | False | int | The number of workers active in the action. Since we're only looking at collective actions, the number must be more than 1. Sometimes the sources do not state a concrete number when reporting. In those cases, lean on the conservative side. For example: "Hundreds of Uber drivers..." --> 100 |
| tags | False | List(str) | Tag the event with a term or word that you feel is relevant but not captured by the other fields. |

In the table above, `action` and `struggles` must contain only the following values:

| Fields | Valid Values | 
| --- | --- |
| action | strike, protest, open_letter, legal_action, union_drive, union_represenation | 
| struggles | ethics, pay_and_benefits, working_conditions, discrimination, unfair_labor_practices, job_security |

## Formatting
When adding an update to the README, use the provided html code below to add a
action. Copy and paste the html snippet under the opening `<div>` tag in the README.

```md
- date: 2018-01-01
- sources: https://www.your.valid/source1, https://www.your.valid/source2
- companies: amazon
- action: protest
- struggles: ethics, discrimination
- worker: 1000
- description: Thousands of people protest a military contract in Queens.
- locations: new_york
- tags: military_contract
- author: organizejs
```

Please note the following aspects:
- If you would like your github username affiliated with the action you added, add an attribute `author` in the `<table>` tag with your github username. If you wish to remain anonymous, skip this step. Keep in mind, your github username will be affiliated with the PR.
- If you add multiple values to a field, make sure the values are comma-seprated. For example, if two types of struggle were involved in the action, it would look like so: `pay_and_benefits, working_conditions`
- DO NOT add additional fields to the file. If you wish to include other information, add it in the description field or as a tag.

## Making A Pull Request (PR)

You can learn about how to make a pull request [here](https://help.github.com/en/articles/creating-a-pull-request). 

When you make a pull request, the request will trigger an Azure pipeline to kick off where it will perform the following:
1. Test that the addition that was made complies with the data fields outlined above - if it does not comply, the Azure pipeline will block the merge.
1. Cleans up the files in /actions
1. Updates the README.md including total actions
1. Updates the `actions.csv` file so that the file is up-to-date

> The cleanup/update uses the `update.py` file described in the "Developer Feature" section below

Shortly after the PR is accepted, you should see your newly added action on the website. The website relies on the `actions.csv` file, so as soon as that file is updated in the CI pipeline, the action should also be reflected on the website. 

## Developer Features

This repository comes with a `update.py` located in the root directory. 

You can use this script to clean up the files in /actions, update the readme or
the csv file.

```sh
# Update files in action folder
$ python update.py --files-cleanup

# Update actions.csv based on files
$ python update.py --files-to-csv

# Update README.md based on files
$ python update.py --files-to-readme
```
