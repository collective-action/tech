# Collective Actions in Tech

This repository documents all collective actions from tech workers in the United States starting from 2016. 

The goal of logging collective action in tech is to give us, tech workers, more insight on worker power in the tech industry. Actions that are considered losses (such as the inability to cause change in the workplace) are also added to this repository since the goal is not to scrutinize the times we've won, but rather to analyze and evaluate on the moments of worker power in tech.

In pursuing this as a public repository, I recognize that this data can be a double-edged sword. Tech workers will have access to the data, but so will our bosses and upper management at our companies. That said, management is organized. They work actively with politicians and laywers to suppress any forms of worker power. We need to be organized too. 

This repository of collective action in tech is meant to be a live document. Feel free to submit PRs or fork the repository.

## Building our data

This respository is mean to document all collective actions from tech workers. Lets define what _collective actions_ and _tech workers_ mean.

__Tech worker__
  - A tech worker is a worker whose income is paid for either directly or indirectly from a tech company.
  
__Collective action__
  - Any kind of concerted activity by workers.
  
For the data to be useful, we'll want to make sure we're collecting enough data with relevant fields on each moment of collective action.

| Field | Description | 
| --- | --- |
| date | While the date may seem trivial, collecting dates may be comlex for multi-day events such as pickets or online petitions. In this repo, we collect only the start date in the format YYYY-MM-DD. |
| company | Since worker power is usually to demand changes from a company, we want to make sure we capture the company in our dataset. Some moments of worker power may not have an associated company. For example, online petitions or a protests against the president may consist of workers from an amalgamation of companies. In which case we can leave this field blank. |
| action | What was the form of the action that took place? |
| employment type | What was the employment type of the workers who took action? FTEs? Contract workers? If there are multipe employment types, they should be listed in the order of most-relevant to least relevant. It is also possible that there is no affiliated employment type, which can be the case for many public petitions. |
| union affiliation | Was a union affiliated? And if so, which one? |
| worker count | The number of workers active in the action. Since we're only looking at collective actions, the number must be more than 1. |
| struggle | The topic of struggle that caused the action. | 
| source | The url of a reliable source that has reported on this event. |

### List of Actions
<table id="collective-actions-in-tech">
  <tr>
    <td>date</td>
    <td>company</td>
    <td>action</td>
    <td>employment type</td>
    <td>union affiliation</td>
    <td>worker count</td>
    <td>struggle</td>
    <td>source</td>
  </tr>
  <tr data-author="organizejs">
    <td class="date">18-01-2017</td>
    <td class="company">Palantir</td>
    <td class="action">Protest</td>
    <td class="employment_type">None</td>
    <td class="union_affiliation">None</td>
    <td class="worker_count">50</td>
    <td class="struggle_type">Ethics</td>
    <td class="source">https://techcrunch.com/2017/01/18/tech-employees-protest-in-front-of-palantir-hq-over-fears-it-will-build-trumps-muslim-registry/</td>
  </tr>
  <tr data-author="organizejs">
    <td class="date">24-07-2017</td>
    <td class="company">Facebook</td>
    <td class="action">Union represenation</td>
    <td class="employment_type">Vendor</td>
    <td class="union_affiliation">Unite Here Local 19</td>
    <td class="worker_count">500</td>
    <td class="struggle_type">Wages, Health benefits</td>
    <td class="source">http://unitehere.org/press-releases/cafeteria-workers-at-facebook-unionize-continuing-movement-for-a-more-inclusive-silicon-valley/</td>
  </tr>
  <tr data-author="organizejs">
    <td class="date">13-12-2016</td>
    <td class="company">None</td>
    <td class="action">Online pledge</td>
    <td class="employment_type">None</td>
    <td class="union_affiliation">None</td>
    <td class="worker_count">2843</td>
    <td class="struggle_type">Ethics</td>
    <td class="source">https://neveragain.tech/</td>
  </tr>
</table>

