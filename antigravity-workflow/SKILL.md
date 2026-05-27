---
name: antigravity-workflow
description: Simulate the workflow used by antigravity with high emphasis on concise, terse, non-verbose deliverables using Cursor Canvas
disable-model-invocation: true
---

# Antigravity workflow

Simulates the workflow used by the antigravity development cycle of code research, implementation plan development, approval, implementation, and review using the Cursor Canvas capability.

## Tasks
**use the TODO tool to track tasks**

### 1. Review request & Research
- Standardize a unique `{task}` slug as a lowercase kebab-case identifier (e.g., `fix-auth-bug`).
- **Resuming Tasks**: If resuming, load the existing Cursor Canvas workspace for the task, skip completed phases, and post a concise chat summary of remaining checklist items and resumption point.
- **Research codebase & Data**: Find relevant files, trace logical flows, and build a full understanding of the scope of changes, potential impacts, risks, and side-effects. Perform rigorous mathematical, statistical, or logical research if required. **Do NOT begin or complete any actual implementation work during the Research or Planning phases.**
- **Document Research**: Populate the **Research Results** section in the canvas immediately after the research is complete, ensuring a target audience of a data scientist.

### 2. Develop an implementation plan
Develop a highly concise, terse plan and checklist using the Cursor Canvas capability. Create a single interactive Cursor Canvas workspace which integrates the plan, live task tracker, verification results, and walkthrough in one dynamic panel.

#### Rules for Brevity & Efficiency:
1. **No Fluff**: Keep plans and dashboards extremely crisp. Avoid long-winded paragraphs or verbose descriptions.
2. **Programmatic Notebook Edits**: When editing Jupyter Notebooks (`.ipynb`), write and execute a temporary Python helper script to parse and programmatically inject new cells rather than rewriting raw JSON text directly to save token context and prevent corruption of existing serialized outputs.

#### Canvas Template:
Below is the boilerplate structure for the interactive workspace canvas containing the exact sections of the research results, implementation plan, and walkthrough:

```tsx
import React from "react";
import {
  Stack,
  Row,
  Grid,
  H1,
  H2,
  H3,
  Text,
  Callout,
  Card,
  CardBody,
  CardHeader,
  Pill,
  Button,
  Divider,
  TodoList,
  Table,
  Stat,
  Checkbox,
  TextArea,
  LineChart,
  BarChart,
  useCanvasState,
  useHostTheme,
  TodoItem
} from "cursor/canvas";

export default function TaskWorkspace() {
  const theme = useHostTheme();
  
  // Phase tabs: "planning" | "tracker" | "verification" | "review" | "research"
  const [phase, setPhase] = useCanvasState<string>("phase", "planning");
  const [approved, setApproved] = useCanvasState<boolean>("approved", false);
  
  // Dynamic checklist tasks (for Option B Tracker)
  const [todos, setTodos] = useCanvasState<TodoItem[]>("todos", [
    { id: "step-1", content: "Implement feature logic and tests", status: "pending" },
    { id: "step-2", content: "Run automated verification", status: "pending" },
    { id: "step-3", content: "Final review and walkthrough", status: "pending" }
  ]);

  // Multiselect Question 1 State (Array of selected values)
  const [questionSelections, setQuestionSelections] = useCanvasState<string[]>("questionSelections", []);
  
  // Free text answer state
  const [otherFreeText, setFreeText] = useCanvasState<string>("otherFreeText", "");

  // Inline comments/feedback on specific sections/bullet points
  const [feedbackSummary, setFeedbackSummary] = useCanvasState<string>("feedbackSummary", "");
  const [feedbackProposedChanges, setFeedbackProposedChanges] = useCanvasState<string>("feedbackProposedChanges", "");

  const handleTodoClick = (clickedTodo: TodoItem) => {
    setTodos(prev => prev.map(t => {
      if (t.id === clickedTodo.id) {
        const nextStatus = t.status === "pending" ? "in_progress" :
                           t.status === "in_progress" ? "completed" : "pending";
        return { ...t, status: nextStatus };
      }
      return t;
    }));
  };

  const handleSelectionToggle = (val: string) => {
    setQuestionSelections(prev => 
      prev.includes(val) ? prev.filter(v => v !== val) : [...prev, val]
    );
  };

  const completedCount = todos.filter(t => t.status === "completed").length;

  return (
    <Stack gap={16} style={{ padding: 16, background: theme.bg.editor, color: theme.text.primary, minHeight: "100vh" }}>
      <Row justify="space-between" align="center">
        <Stack gap={4}>
          <H1>Task Workspace: {title}</H1>
          <Text tone="secondary" size="small">Slug: {task_slug}</Text>
        </Stack>
        <Row gap={8}>
          <Pill active={phase === "planning"} onClick={() => setPhase("planning")}>1. Planning</Pill>
          <Pill active={phase === "tracker"} onClick={() => setPhase("tracker")}>2. Task Tracker</Pill>
          <Pill active={phase === "verification"} onClick={() => setPhase("verification")}>3. Verification</Pill>
          <Pill active={phase === "review"} onClick={() => setPhase("review")}>4. Walkthrough</Pill>
          <Pill active={phase === "research"} onClick={() => setPhase("research")}>5. Research Results</Pill>
        </Row>
      </Row>

      <Divider />

      <Grid columns={3} gap={16}>
        <Stat value={approved ? "Approved" : "Needs Review"} label="Plan Status" tone={approved ? "success" : "warning"} />
        <Stat value={`${completedCount} / ${todos.length}`} label="Tasks Completed" tone={completedCount === todos.length ? "success" : "info"} />
        <Stat value={phase.toUpperCase()} label="Current Phase" />
      </Grid>

      {phase === "planning" && (
        <Stack gap={16}>
          <H2>Implementation Plan: {title}</H2>
          
          <Stack gap={8}>
            <Text>{summary}</Text>
            {/* Inline comment field for Paragraph/Summary Section */}
            <TextArea 
              value={feedbackSummary} 
              onChange={setFeedbackSummary} 
              placeholder="Add inline feedback or corrections on the summary paragraph..." 
              rows={2}
            />
          </Stack>

          <H3>User Review Required</H3>

          <Callout tone="danger" title="RISKS">
            <Stack gap={4}>
              <Text>1. {risk_1}</Text>
            </Stack>
          </Callout>

          <Callout tone="warning" title="IMPORTANT">
            <Stack gap={4}>
              <Text>1. {important_note_1}</Text>
            </Stack>
          </Callout>

          <Card>
            <CardHeader>Open Questions (Multi-Select & Free-Text)</CardHeader>
            <CardBody>
              <Stack gap={16}>
                <Stack gap={8}>
                  <Text weight="semibold">1. Which authentication strategies should we support? (Multiselect)</Text>
                  <Checkbox 
                    checked={questionSelections.includes("strategy-jwt")} 
                    onChange={() => handleSelectionToggle("strategy-jwt")} 
                    label="Option A: JWT (Stateless, standard Token-based authentication)" 
                  />
                  <Checkbox 
                    checked={questionSelections.includes("strategy-session")} 
                    onChange={() => handleSelectionToggle("strategy-session")} 
                    label="Option B: Sessions (Stateful Cookie-based tracking)" 
                  />
                  <Checkbox 
                    checked={questionSelections.includes("strategy-oauth")} 
                    onChange={() => handleSelectionToggle("strategy-oauth")} 
                    label="Option C: OAuth 2.0 (Social/Single Sign-On Integration)" 
                  />
                </Stack>
                <Stack gap={8}>
                  <Text weight="semibold">Notes or Alternative Preferences:</Text>
                  <TextArea 
                    value={otherFreeText} 
                    onChange={setFreeText} 
                    placeholder="Specify any other preferences, constraints, or custom options..." 
                    rows={3}
                  />
                </Stack>
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>Proposed Changes</CardHeader>
            <CardBody>
              <Stack gap={12}>
                <Stack gap={8}>
                  <Text>• <Code>src/utils.ts</Code>: Refactor helper logic to improve performance.</Text>
                  <Text>• <Code>src/index.ts</Code>: Integrate the updated helper functions.</Text>
                </Stack>
                {/* Inline comment field for Proposed Changes List */}
                <TextArea 
                  value={feedbackProposedChanges} 
                  onChange={setFeedbackProposedChanges} 
                  placeholder="Provide feedback on proposed changes, file targets, or logic details..." 
                  rows={2}
                />
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>Verification Plan</CardHeader>
            <CardBody>
              <Grid columns={2} gap={16}>
                <Stack gap={4}>
                  <Text weight="semibold">Automated Verification</Text>
                  <Text tone="secondary">1. {automated_verification_step_1}</Text>
                </Stack>
                <Stack gap={4}>
                  <Text weight="semibold">Manual Verification</Text>
                  <Text tone="secondary">1. {manual_verification_step_1}</Text>
                </Stack>
              </Grid>
            </CardBody>
          </Card>

          {!approved && (
            <Callout tone="info" title="User Review Required">
              <Row gap={12} align="center">
                <Text>Please review this plan. If you agree, click Approve or type APPROVED in chat.</Text>
                <Button variant="primary" onClick={() => setApproved(true)}>Approve Plan</Button>
              </Row>
            </Callout>
          )}
        </Stack>
      )}

      {phase === "tracker" && (
        <Stack gap={16}>
          <H2>Interactive Task Tracker</H2>
          <Text tone="secondary">Click a task to cycle status: Pending → In Progress → Completed.</Text>
          <TodoList todos={todos} onTodoClick={handleTodoClick} />
        </Stack>
      )}

      {phase === "verification" && (
        <Stack gap={16}>
          <H2>Verification Status</H2>
          <Callout tone="info" title="Automated & Manual Verification">
            <Text>Record test and lint results here during the verification step.</Text>
          </Callout>
        </Stack>
      )}

      {phase === "review" && (
        <Stack gap={16}>
          <H2>Walkthrough: {title}</H2>
          <Text>{summary}</Text>

          <H3>User Review Required</H3>

          <Callout tone="danger" title="RISKS">
            <Stack gap={4}>
              <Text>1. {risk_1}</Text>
            </Stack>
          </Callout>

          <Callout tone="warning" title="IMPORTANT">
            <Stack gap={4}>
              <Text>1. {important_note_1}</Text>
            </Stack>
          </Callout>

          <Card>
            <CardHeader>Changes Made</CardHeader>
            <CardBody>
              <Stack gap={8}>
                <Text>• <Code>src/utils.ts</Code>: Implemented and fully tested optimized helper logic.</Text>
                <Text>• <Code>src/index.ts</Code>: Successfully integrated the new changes.</Text>
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>Verification Results</CardHeader>
            <CardBody>
              <Grid columns={2} gap={16}>
                <Stack gap={4}>
                  <Text weight="semibold">Automated Verification</Text>
                  <Text tone="secondary">{automated_verification_results}</Text>
                </Stack>
                <Stack gap={4}>
                  <Text weight="semibold">Manual Verification</Text>
                  <Text tone="secondary">{manual_verification_instructions_for_user}</Text>
                </Stack>
              </Grid>
            </CardBody>
          </Card>
        </Stack>
      )}

      {phase === "research" && (
        <Stack gap={16}>
          <H2>Research Results</H2>
          <Text tone="secondary">Target Audience: Data Scientist Reviewer</Text>

          <Card>
            <CardHeader>Research Methods</CardHeader>
            <CardBody>
              <Text>{research_methods_description}</Text>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>Assumptions</CardHeader>
            <CardBody>
              <Stack gap={4}>
                <Text>• {assumption_1}</Text>
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>Results & Key Graphs</CardHeader>
            <CardBody>
              <Stack gap={12}>
                <Text>{results_summary}</Text>
                {/* 
                  Use LineChart, BarChart, or PieChart from cursor/canvas to render key graphs.
                  Alternatively, use inline SVG if rendering specific custom data visualisations.
                */}
                <Text tone="secondary" italic>[Key Graph Visualization Placeholder / Chart]</Text>
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>Conclusions & Findings</CardHeader>
            <CardBody>
              <Stack gap={4}>
                <Text>• {conclusion_1}</Text>
              </Stack>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>Reproduce Results</CardHeader>
            <CardBody>
              <Stack gap={4}>
                <Text weight="semibold">Execute the following commands to reproduce plots and findings:</Text>
                <Code>{reproduce_commands}</Code>
              </Stack>
            </CardBody>
          </Card>
        </Stack>
      )}
    </Stack>
  );
}
```

### 3. User review
- Create the interactive Cursor Canvas workspace and provide a relative link for the user to open beside the chat.
- Provide a highly concise, high-level summary of proposed changes **(maximum 3-4 bullets total)** in the chat.
- Ask the user to reply with **APPROVED** (or click Approve in the canvas UI) to proceed. Repeat if revisions are requested.
- **DO NOT proceed to Implementation without explicit "APPROVED" sign-off.** Once approved, mark as approved in the canvas state.

### 4. Implementation
- Execute changes sequentially in the main chat.
- As each step completes, update the checklist state in the interactive canvas.
- Maintain exact indentation/formatting; avoid placeholder code.

### 5. Verification
- Update the canvas workspace to the verification phase.
- Execute all automated verification checks. 
- If checks fail: increment verification attempts, record test/linter error in the verification panel of the canvas, apply fixes, and re-run.
- If unresolved after **3 attempts**, halt, report logs, and ask for user guidance.
- **DO NOT proceed to review changes until all Automated Verification checks pass.**

### 6. Review changes
- Update the canvas workspace to the review/walkthrough phase.
- **Enforce Walkthrough Boilerplate**: Ensure that the Walkthrough panel (`review` phase tab) strictly retains all specified layout sections from the Phase 2 template (Title & Summary, H3 User Review Required, Callout RISKS, Callout IMPORTANT, Card Changes Made, and Card Verification Results).
- **Update Research Results**: Review and update the **Research Results** section of the canvas (now sitting as Phase 5 after the walkthrough) with any final metrics, verified assumptions, polished key graphs, refined conclusions, and updated reproduction commands that were established/refined during the implementation/verification steps. Ensure it strictly retains all layout sections from the Phase 2 template (Research Methods, Assumptions, Results & Key Graphs, Conclusions & Findings, Reproduce Results).
- Provide a very brief summary in the chat including:
  - A 1-2 sentence overview.
  - A numbered list of completed logical steps.
  - A relative link to the interactive walkthrough canvas.
