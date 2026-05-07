---
name: generate-research-project
description: Read a ticket or linked README, optionally create a new working git branch, set up the folder structure for the research, and write a README.md about the project
disable-model-invocation: true
---

Determine the project source:
- If a ticket is provided, use the MCP to access the ticket in Jira.
- If no ticket is provided but a README is linked, read that README and use it as the project source instead. Use the directory containing that README as the project folder unless the user explicitly provides a different folder.
- If neither a ticket nor README is provided, ask the user for one before continuing.

Check whether the selected project folder is inside a git repo:
- If git is available there, start by checking out the main/master branch of the git repo and ensuring it is up to date.
- If git is not available there, skip all git checkout, pull, and branch creation steps.

When git is available, create a branch using:
- The ticket name followed by short title when using a ticket (i.e. DST-234_some_research)
- A short kebab-case title derived from the README when using a README

In the folder provided by the user (ask which folder if none is provided), make a new folder using the same name as the branch. When using a linked README and no folder is provided, use the README's directory.
If git is not available, use the same naming convention to create the folder name even though no branch is created.

For the new folder the following should be built
|- README.md
|- Research_plan.md
|- results/
|- research_tasks/

README.md should contain:
- A link to the ticket and a summary of the issues related to the ticket, when using a ticket
- A link to the source README and a summary of the research context from that README, when using a README
- If `llm_wiki/` exists in the repo, a "Related wiki pages" section listing relevant existing wiki pages with markdown links — read `llm_wiki/index.md` to identify candidates. See the `llm_wiki` skill's "Research workflow integration" section.

All other files and folders should have an empty readme placed in the folders.
