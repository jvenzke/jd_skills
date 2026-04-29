---
name: generate-research-project
description: Read a ticket or linked README, create a new working git branch, set up the folder structure for the research, and write a README.md about the project
---

start by checking out the main/master branch of the git repo and ensuring it is up to data 

Determine the project source:
- If a ticket is provided, use the MCP to access the ticket in Jira.
- If no ticket is provided but a README is linked, read that README and use it as the project source instead.
- If neither a ticket nor README is provided, ask the user for one before continuing.

Create a branch using:
- The ticket name followed by short title when using a ticket (i.e. DST-234_some_research)
- A short kebab-case title derived from the README when using a README

In the folder provided by the user (ask which folder if non is proviced), make a new folder using the same name as the branch.

For the new folder the following should be built
|- README.md
|- Research_plan.md
|- results/
|- research_tasks/

README.md should contain:
- A link to the ticket and a summary of the issues related to the ticket, when using a ticket
- A link to the source README and a summary of the research context from that README, when using a README

All other files and folders should be left blank 
