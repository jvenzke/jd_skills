---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
disable-model-invocation: true
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer. 

Format the questions as a markdown numbered list, with each candidate answer as a lettered sub-bullet indented under its question:

```
1. {details of question}
   - a) (recommended) {answer text a}
   - b) {answer text b}
   - c) ...

2. {details of next question}
   - a) (recommended) {answer text a}
   - b) {answer text b}
```

Ask all questions in 1 pass. Ask them directly in the chat and pause for my response. Only repeat a pass if answering a question was blocked or changed by the answers I gave. 

If a question can be answered by exploring the codebase, explore the codebase instead.

After alignment has completed, provide an brief in chat summary detailing the results. 