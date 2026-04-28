---
name: generate-research-project
description: Read a ticket, create a new working git branch, setup the folder struture for the research, and write a readme.md about the project
---

start by checking out the main/master branch of the git repo and ensuring it is up to data 

use the MCP to access the ticket in jira. 

Create a branch with the ticket name followed by short title (i.e. DST-234_some_research)

In the folder provided by the user (ask which folder if non is proviced) make a new foleder named ticket name followed by short title

For the new folder the following should be built
|- README.md
|- Research_plan.md
|- results/
|- research_tasks/
|- research_workspace/

README.md should containt a link to the ticket and summarize the issues related to the ticket 

All other files and folders should be left blank 
