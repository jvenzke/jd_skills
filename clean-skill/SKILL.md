---
name: clean-skill
description: Used to clean up a skill that has been worked on. It focuses on how an implementing agent will work with the skill
disable-model-invocation: true
---
Review the skill the user has provided. Without looking at any other context, can you note anything that is unneeded or unclear. The main goal is to flag out things that are not written for the impelmenting agent. Please provide a numbered list of any problems. 
For each problem provide a recommended solution and 2 other letter labeled options. The user should be able to provide a response like `1a {notes} ...`.

Stop for my response prior to making any changes. 

After getting a respones, write an in chat summary of the changes and ask for explicit approval before making the change.
