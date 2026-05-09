# Index
## Create PRD: https://hackmd.io/@starfysh/aidt-create-prd
### Generate Tasks (for baseline comparison): https://hackmd.io/@starfysh/aidt-generate-tasks
### Generate Tasks (Updated approach that includes a form of TDD lite): https://hackmd.io/@starfysh/aidt-generate-tasks-testaware
### Process Task List (with some customizations to use Claude Code's built-in todo tracker): https://hackmd.io/@starfysh/aidt-process-task-list
### Commands - Dashboard (my addition) Gives a visualization of status: https://hackmd.io/@starfysh/aidt-commands-dashboard
### Commands - Generate Tasks Test Aware: https://hackmd.io/@starfysh/aidt-command-generate-tasks-testaware
### Commands - Process Tasks: https://hackmd.io/@starfysh/aidt-command-process-tasks

# The process should be straight forward:
    - Copy 6 + 3 to your folder
    - Generate tasks based on a PRD already complete (or do side-by-side)
    - Process the test aware tasks
    - Compare the resulting code to see if you get higher quality results.


# Rule: Generating a Product Requirements Document (PRD)
## Goal
To guide an AI assistant in creating a detailed Product Requirements Document (PRD) in Markdown format, based on an initial user prompt. The PRD should be clear, actionable, and suitable for a junior developer to understand and implement the feature.

## Process
### Receive Initial Prompt: The user provides a brief description or request for a new feature or functionality.
### Ask Clarifying Questions: Before writing the PRD, the AI must ask clarifying questions to gather sufficient detail. The goal is to understand the "what" and "why" of the feature, not necessarily the "how" (which the developer will figure out). Make sure to provide options in letter/number lists so I can respond easily with my selections.
### Review and Simplify: Before generating the PRD, challenge complexity assumptions and identify the simplest viable solution. Strip requirements to core value-delivering functionality.
### Generate PRD: Based on the initial prompt, clarifying answers, and simplification review, generate a PRD using the structure outlined below.
### Save PRD: Save the generated document as prd-[feature-name].md inside the /tasks directory.
### Clarifying Questions (Examples)
### The AI should adapt its questions based on the prompt, but here are some common areas to explore:

## Problem/Goal: "What problem does this feature solve for the user?" or "What is the main goal we want to achieve with this feature?"
### Target User: "Who is the primary user of this feature?"
### Core Functionality: "Can you describe the key actions a user should be able to perform with this feature?"
### User Stories: "Could you provide a few user stories? (e.g., As a [type of user], I want to [perform an action] so that [benefit].)"
### Acceptance Criteria: "How will we know when this feature is successfully implemented? What are the key success criteria?"
### Scope/Boundaries: "Are there any specific things this feature should not do (non-goals)?"
### Data Requirements: "What kind of data does this feature need to display or manipulate?"
### Design/UI: "Are there any existing design mockups or UI guidelines to follow?" or "Can you describe the desired look and feel?"
### Edge Cases: "Are there any potential edge cases or error conditions we should consider?"
### Simplification: "What's the simplest way to achieve this core goal?" and "Could this be built using existing components?"
### Scope Reduction: "What's the minimum viable version that delivers value?" and "Which parts could be deferred to v2?"

## PRD Structure
The generated PRD should include the following sections:

### Introduction/Overview: Briefly describe the feature and the problem it solves. State the goal.
### Goals: List the specific, measurable objectives for this feature.
### User Stories: Detail the user narratives describing feature usage and benefits.
### Functional Requirements: List the specific functionalities the feature must have. Use clear, concise language (e.g., "The system must allow users to upload a profile picture."). Number these requirements.
### Implementation Approach: Describe the simplest technical approach. Must justify any complexity and list simpler alternatives considered.
### Non-Goals (Out of Scope): Clearly state what this feature will not include to manage scope.
### Design Considerations (Optional): Link to mockups, describe UI/UX requirements, or mention relevant components/styles if applicable.
### Technical Considerations (Optional): Mention any known technical constraints, dependencies, or suggestions (e.g., "Should integrate with the existing Auth module").
### Success Metrics: How will the success of this feature be measured? (e.g., "Increase user engagement by 10%", "Reduce support tickets related to X").
### Open Questions: List any remaining questions or areas needing further clarification.
### Target Audience
### Assume the primary reader of the PRD is a junior developer. Therefore, requirements should be explicit, unambiguous, and avoid jargon where possible. Provide enough detail for them to understand the feature's purpose and core logic.

# Output
## Format: Markdown (.md)
## Location: /tasks/
## Filename: prd-[feature-name].md
## Final instructions
- Do NOT start implementing the PRD
- Make sure to ask the user clarifying questions
- Review answers and challenge complexity before writing PRD
- Take the user's answers and simplification review to generate the PRD
