# Contribution Guidelines

One of the goals of this repo is to make sure that the data is as update-to-date as possible, so please feel free to make additions to the dataset as current events unfold!

To contribute, please use pull requests to add to the repo so that new additions can be checked for formatting, accuracy and validity.

This document will cover how to contribute:
1. Defining "Collective Action"
1. How to Contribute on Airtable
1. How To Contribute on GitHub
1. Data Fields
1. Formatting Guidelines
1. Developer Features

## Defining "Collective Action"

Events must be "collective" and contain "evidence of action" by currently or recently employed "tech workers". All events must be publicly reported on in a publication.

(1) "Collective". Must involve a minimum of two employees who recognize themselves as a group united by a shared cause and/or issue. The cause and/or issue should be relevant to a broader public, defined as a community which is not directly related to the company through employment or financial ties. The broader public does not include company shareholders, businesses with shared interests, or owners of company property, which include consumers of company products. An action that would typically not be deemed relevant to a broader public on its own merit may qualify if the group presents an argument that it is occurring in response to a cause and/or issue that is relevant to a broader public (e.g. an employee who is believed to have been fired as retaliation for a recent protest). 

(2) "Evidence of action". Must involve an attempt to present the cause and/or issue outside of the immediate group. Actions may be either internal (available or visible only to other employees) or external (available or visible to the broader public). Lawsuits may be be included if they are granted class action status or if they incite additional collective action. Actions should not be the initiated by company management.

(3) "Tech workers". Defined as current or recently employed (within the last year) workers in the tech industry. Tech industry includes but is not limited to information technology, Internet, hardware, software. Does not include adjacent industries, e.g. digital media (e.g. Vox, Buzzfeed) or the video game industry (unless the company's primary business is in any of the above categories, e.g. Niantic). Does include online retailers (e.g. Amazon, Wayfair) and social media companies. Academics whose research concerns technology and students or interns who are preparing to enter the tech industry can be considered tech workers. 

**If you are unsure about whether an action fits the definition, we encourage you to contribute anyways! We are always interested in hearing about new types of collective actions. The above definition may evolve over time.**

## How To Contribute on Airtable

Airtable is the easiest way to add to the repository. Simply fill out the form located here: https://airtable.com/shrT1A5QWKtquXv3D. More formatting directions are included on the form itself. Once your addition is approved, it will update to Github.

## How To Contribute on GitHub

There are two ways that you can add or update collective actions in this repo: updating the `actions.csv` file __or__ the `.json` files inside of the `actions/` folder. Only update one or the other. Once you've made your update, commit those changes to a new branch and create a pull-request into the master branch.

Once the changes get pushed to the repo, the CI pipeline will automatically sync the content on the README.md, the website, and the CSV, and the actions-folder. By default, the CI pipeline will synchronize with the `actions/` folder. However, if you choose to update the `actions.csv` file, you'll want the CI pipeline to synchronize with the `actions.csv` instead. To do this, you'll need to add an empty file, called `CSV_FLAG` (Note that there are no extensions to the file), to the root directory of the repository before making your PR.  This additional file will notify the CI pipeline to synchronize with the `actions.csv` file instead of performing its default behavior, which is to synchronize with the `actions/` folder. 

__Updating the actions folder__

Create a new json file under the '/actions' folder in the root directory of this repo. We recommend naming it something unique like `<username>-<action>.json` so that it doesn't conflict with any other file.

Once your changes are committed, the CI pipeline will automatically sort all the events inside the `actions/` folder. It will also update the `README.md` and the `actions.csv` accordingly.

__Updating the csv__

If you plan on editing or adding multiple events, we recommend using this method. Simply update the fields of the `actions.csv` or add new collective actions to the list. If you are adding new events, simply add them on at the end of the CSV file as new rows. Once your changes are committed, the CI pipeline will automatically sort all the events and update the CSV file. It will also update the `README.md` and the `actions/` folder accordingly. Don't forget to add a new file, called `CSV_FLAG` (with no extensions) to the root directory of the repo before making your PR.

## Data Fields

When adding a new action, collect data on the following fields. If one or more
of the fields are not applicable, you can omit the field. However, you cannot
add a new field at this time. If there is additional information you'd like to
include, add it in the description field.

> Take note of the plurality of the fields. `actions` and `sources` are plural. 

| Field | Required | Type | Description |
| --- | --- | --- | --- |
| date | True | YYYY/MM/DD | While the date may seem trivial, collecting dates may be comlex for multi-day events such as pickets or online petitions. In this repo, we collect only the start date of the action in the format YYYY/MM/DD. |
| sources | True | List(url) | The url(s) of reliable sources that has reported on this event. |
| actions | True | List(str) | What was the form of the action that took place? (`union_drive`, `union_representation`, `open_letter`, `strike`, `protest`, `legal_action`) |
| struggles | True | List(str) | The kind of struggle workers are standing up against. (`pay_and_benefits`, `working_conditions`, `unfair_labor_practices`, `job_security`, `ethics`, `discrimination`)| 
| employment_types | True | List(str) | The employment type(s) of the workers involved in the collective action. (`white_collar_workers`, `blue_collar_workers`, `in_house_workers`, `contract_workers`, `gig_workers`, `na`)|
| description | True | str | A short paragraph describing the event where you can include information that isn't covered in the fields above. Multiple paragraphs are not allowed in this field. |
| locations | False | List(List(str)) | The location(s) of the action, or whether it was online. `[["<city1>", "<state1>", "<country1>"], ["<city2>", "<state2>", "<country2>"]]` |
| companies | False | List(str) | Which company are workers are standing up against? Some moments of worker power may not have an associated company. For example, online petitions or a protests against the president may consist of workers from an amalgamation of companies. In which case we can omit this field. |
| workers | False | int | The number of workers active in the action. Since we're only looking at collective actions, the number must be more than 1. Sometimes the sources do not state a concrete number when reporting. In those cases, lean on the conservative side. For example: "Hundreds of Uber drivers..." --> 100 |
| tags | False | List(str) | Tag the event with a term or word that you feel is relevant but not captured by the other fields. One good thing to add is the kind of worker who is taking action. Please see below for more information on tags. |

In the table above, `actions`, `struggles`, `employment_type` must contain only the following values:

| Fields | Valid Values | 
| --- | --- |
| actions | `strike`, `protest`, `open_letter`, `legal_action`, `union_drive`, `union_represenation` | 
| struggles | `ethics`, `pay_and_benefits`, `working_conditions`, `discrimination`, `unfair_labor_practices`, `job_security` |
| employment_type | `white_collar_workers`, `blue_collar_workers`, `in_house_workers`, `contract_workers`, `gig_workers`, `na` |

If any of the following __tags__ are applicable, please add them to the action:

`coworker_solidarity`, `industry_solidarity`, `international_solidarity`, `lgbtq`, `fund_raising`, `mijente`, `temporary_workers_of_america`, `military_contracts`, `trade_war`, `seiu`, `law_enforcement`, `sexism`, `muslim_registry`, `academics`, `moderators`, `gig_workers_rising`, `twc`, `unite_here`, `climate_change`, `ice`, `ai`, `trump`, `retaliation`, `cbp`, `teamster`, `immigration`, `students`, `coronavirus`, `antiracism`,`blm`, `None` (if none apply)

## Formatting
Add your data using the standard JSON convention:

```json
{
  "date": "2018/01/15",
  "sources": [
    "https://www.your.valid/source1",
    "https://www.your.valid/source2"
  ],
  "actions": [
    "protest",
    "open_letter"
  ],
  "struggles": [
    "ethics",
    "discrimination"
  ],
  "employment_types": [
    "white_collar_workers",
    "in_house_workers"
  ],
  "description": "Thousands of people protest a military contract in Queens.",
  "locations": [
    [
      "new_york",
      "usa"
    ],
    [
      "online"
    ]
  ],
  "companies": [
    "amazon"
  ],
  "workers": 1000,
  "tags": [
    "military_contract",
    "delivery_workers"
  ],
  "author": "organizejs"
}
```

Please note the following aspects:
- We expect the standard JSON format. You can use a [JSON validator](https://jsonlint.com/) to check that its correctly formatted.
- If you would like your github username affiliated with the action you added, add an attribute `author` in the `<table>` tag with your github username. If you wish to remain anonymous, skip this step. Keep in mind, your github username will be affiliated with the PR.
- DO NOT add additional fields to the file. If you wish to include other information, add it in the description field or as a tag.

## Making A Pull Request (PR)

You can learn about how to make a pull request [here](https://help.github.com/en/articles/creating-a-pull-request). 

When you make a pull request, the request will trigger an Azure pipeline to kick off where it will perform the following:
1. Test that the addition that was made complies with the data fields outlined above - if it does not comply, the Azure pipeline will block the merge.
1. Cleans up the files in /actions
1. Updates the README.md including total actions
1. Updates the `actions.csv` and `actions.json` files so that the file is up-to-date

> The cleanup/update uses the `update.py` file described in the "Developer Feature" section below

Shortly after the PR is accepted, you should see your newly added action on the website. The website relies on the `actions.json` file, so as soon as that file is updated in the CI pipeline, the action should also be reflected on the website. 

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

# Update actions.json based on files
$ python update.py --files-to-json
```
