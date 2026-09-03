---
name: research-first
description: >-
  Web-landscape research and alignment before other work. Writes
  field_research.md, asks numbered option questions grounded in that brief,
  then continues the user's task. Use when the user invokes research-first
  or wants recent field trends before implementing.
disable-model-invocation: true
---

# Research-first

Before planning or implementing the user's task: write a sourced field brief,
align on blocking forks, then do the work using those decisions.

If another workflow skill is attached in this chat, finish this gate first,
then follow that skill. Treat `field_research.md` as required input.

## Artifact

In the target repo, create `.working_items/{task}/field_research.md` if
missing. `{task}` is a lowercase kebab-case slug from the request.

```markdown
# field_research — {task}

## Orientation

## Landscape

## Questions

## Decisions
```

| Section | Write |
| --- | --- |
| **Orientation** | Problem + local stack (short) |
| **Landscape** | Default approach, 1–3 alternatives, what changed (~2–3 years), implications for this task. URL on every major claim |
| **Questions** | The numbered questions as asked in chat (write when asking) |
| **Decisions** | After the user replies: id → choice, recommended vs actual, one-line rationale |

Custom replies are allowed (`1: use X instead`).

## Resume

On start, read `field_research.md` if it exists.

- **Landscape** + filled **Decisions** → skip to **Do the work**.
- **Landscape** without **Decisions** → skip to **Align** (reuse **Questions**).
- Missing or incomplete **Landscape** → start at **Orient**.
- User said `refresh` / `redo research` → start at **Orient**.

## Workflow

**Do not plan, deep-dive the codebase, or implement until Decisions are filled.**

### 1. Orient

Read the request and enough of the repo to name the stack and problem
(languages, existing libraries, README). Stop there.

### 2. Landscape

Search and fetch primary sources from roughly the last 2–3 years (official
docs, RFCs, major changelogs, well-known engineering posts). Fill:

1. Current default approach
2. 1–3 serious alternatives
3. What changed recently
4. Implications for this task

A handful of searches is enough. If the web is thin, say so in **Landscape**
and still align.

Write the full brief to `field_research.md`. Do not paste the file in chat.

### 3. Align

Ask blocking questions grounded in the landscape: which approach, library, or
tradeoff to take, plus constraints only the user knows. Do not ask what the
repo can answer.

One numbered pass of independent questions. Options alphabetical (`a)`, `b)`,
…); mark **(recommended)**. User replies with ids (`1b 2a`) or a short custom
answer.

```
1. Which HTTP client style?
   a) (recommended) Native fetch
   b) Axios
   c) Got
```

In chat: path to the file, 5–8 bullets (default, alternatives, what changed,
implications), then the questions. Pause.

Follow-ups only when an answer unlocks another blocking choice.

### 4. Log decisions

Fill **Decisions**. That reply is the gate — do not wait for **APPROVED**.

### 5. Do the work

Re-read **Decisions** (and **Landscape** as needed). Then carry out the user's
task in this chat.
