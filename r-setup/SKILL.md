---
description: "Load a Jira ticket and set up the file structure for research"
disable-model-invocation: true
---
# Setup Research

## Input
- The user will provide a folder to set up the research project in 
- The user will either provide context in the prompt or a link to a Jira ticket
   - For a Jira ticket: Use the MCP to access the ticket
## Output 
- Setup the initial file structure (outlined below)
- Prompt user to work on `input_plan.md` then call `r-plan`

## Progress tracking

Use the **Todo** feature to track each setup step (folder layout, `README.md`, `input_plan.md`, `research_plan.md`, `next_step.md`, `research_log.md`). Create todo items when you start and mark each item completed as you finish it.

## Folder setup 
Generate the following files 
```text
├── README.md
├── input_plan.md
├── next_step.md
├── research_plan.md
├── research_log.md
├── Canvases/
└── src/
```

## Canvases/

The **`Canvases/`** folder (capital **C**) holds **project copies** of each `.canvas.tsx` dashboard so they live in git and handoffs. During **`r-do`**, the same file is also written to Cursor’s **IDE canvas directory** (`~/.cursor/projects/<workspace>/canvases/` per the canvas skill) so the canvas opens beside chat—both locations must stay in sync.

## README.md contents
- **CRITICAL**: If a `README.md` or `readme.md` already exists, integrate its original content (especially SQL, logs, or problem descriptions) into the new structure; do not overwrite it.
- Link any Jira tickets 
- a short human readable summary of the task
- description of folder layout (include **`Canvases/`** for canvas archives and note that live canvases also use Cursor’s managed `canvases/` path)

## input_plan.md
The file should contain a basic overview of the research goal, useful tables/code/docs

Populate the following with the information you gained from the ticket, initial prompt and other similar research in the code base 
- `{title}`
- `{summary of goal}`
- `{initial plan}` (multiple lines allowed). **Note**: Use sub-bullets for tasks that should be performed together within a single research step.
- `{path/to/code}` (multiple lines allowed)
- `{db.schema.table}` (multiple lines allowed)
- `{path/to/doc}` (multiple lines allowed)

The document should look like the following
```markdown
# Research: {title} 

## Main Research Objective 
{summary of goal}

## Research steps 
Research should be done in a step by step manner. 
Each step should work towards the final goal of the project by breaking the large unknown into small actionable items.
A step should answer one unknown completely by using small atomic sub tasks to verify data quality, test unknowns, and report findings in a digestible manner with supporting graphs
1. {Initial plan}

## Useful files 

### Code files 
- {path/to/code}

### Snowflake tables
- {db.schema.table}

### Docs
- {path/to/doc}
```

# research_plan.md

Populate the following with the information you gained from the ticket, initial prompt and other similar research in the code base 
- `{title}`
- `{summary of goal}`
```markdown
# Research plan: {title} 

## Main Research Objective 
{summary of goal}

## Current step
Summary of the current step that we are working on.

## Working Knowledge
List of known facts about the project. Stale results should be deleted. 

## Result Artifacts 
Links to canvas and plots with short notes on content/context
```

## next_step.md
- A markdown file that maintains the current state of the research. It should say it is a new research project and state `r-plan` is next phase

## research_log.md
Build a file with the following sections 
Populate the following with the information you gained from the ticket, initial prompt and other similar research in the code base
- `{title}` 
```markdown
# Research Log: {title} 

## Task tracking
0. Initial research project setup [Complete]

## Research results 
### Initial setup 
Setup files/folder structure and research plan 
```