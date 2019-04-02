# Contribution Guidelines

One of the goals of this repo is to make sure that the data is as update-to-date as possible, so please feel free to make contributions! 

To contribute, please use pull requests to add to the repo so that new additions can be checked for formatting, accuracy and validity.

## Steps to Contributing
Here are the basic steps to adding a new action using a pull request:
1. Edit the README.md in Github.com
1. The master branch is protected, so you won't be able to merge directly into
   it. Instead, create a new branch (with the event name you want to add in
   the branch title), and open a pull-request.
1. Make a pull request from the branch you've created into the master branch.

When makikng an update to the README, use the provided html code below to add a
row to the table. 
```html
<tr data-author="organizejs">
    <td data-column="action">
    Union represenation
    </td>
    <td data-column="company">
    Facebook
    </td>
    <td data-column="date">
    2017-07-24 00:00:00
    </td>
    <td data-column="employment_type">
    Vendor
    </td>
    <td data-column="source">
    http://unitehere.org/press-releases/cafeteria-workers-at-facebook-unionize-continuing-movement-for-a-more-inclusive-silicon-valley/
    </td>
    <td data-column="struggle_type">
    Wages, Health benefits
    </td>
    <td data-column="union_affiliation">
    Unite Here Local 19
    </td>
    <td data-column="worker_count">
    500
    /td>
</tr>
```
Please note the following aspects:
- If you would like your github username affiliated with the action you added,
  add an attribute `data-author` in the `<tr>` tag with your github username.
  If you wish to remain anonymous, skip this step.
- Each `<td>` tag must have the data attribute `data-column` with its
  associated column.
