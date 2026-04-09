# AGENTS

## Purpose

This file is a short agent entrypoint for this project. It does not override the product or architecture documents. Its job is to tell an agent how to read this repo and which boundaries it must not cross.

## Filename Policy

Most repo documents currently use lowercase filenames. The agent must rely on the real filenames on disk and must not rename them without an explicit user request.

Exception: `PLANS.md` is intentionally uppercase because it is the repo-local ExecPlan standard file.

Canonical files in this directory:
- `project_constitution.md`
- `product_spec.md`
- `document_system.md`
- `architecture.md`
- `agent_system.md`
- `implementation_plan.md`
- `open_questions.md`
- `validation_plan.md`
- `reference_examples.md`

## Required Reading Order

Before doing serious work, the agent must read in this order:
1. `project_constitution.md`
2. `product_spec.md`
3. `document_system.md`
4. depending on the task:
   - `architecture.md`
   - `agent_system.md`
   - `implementation_plan.md`
5. only if genuinely needed:
   - `open_questions.md`
   - `validation_plan.md`
   - `reference_examples.md`

## Document Priority

If documents conflict, use this order:
1. `project_constitution.md`
2. `product_spec.md`
3. `architecture.md`
4. `agent_system.md`
5. `implementation_plan.md`
6. `validation_plan.md`
7. `open_questions.md`

`reference_examples.md` is a helper layer, not a normative one.

## ExecPlans

When a task is larger than a narrow patch, crosses multiple files or nodes, requires meaningful research, a refactor, multi-step implementation, or the user explicitly asks for a plan, the agent must use an ExecPlan according to `PLANS.md`.

This applies especially to:
- large multi-file changes;
- schema or artifact-contract changes;
- work that is likely to last longer than one short session;
- tasks where it is important to leave self-contained, restartable work for another agent or a human.

If an ExecPlan is used:
- the plan must be created and maintained according to `PLANS.md`;
- the plan must remain self-contained and a living document;
- the agent must not ask the user "what next" between milestones unless there is a real blocker or a decision that cannot be made reliably on its own.

## Canonical Truth

- Repo files are the only canonical source.
- The agent must not use chat history as a state source of truth.
- `product_spec.md` governs product rules and the user-visible model.
- `architecture.md` governs artifact semantics, schemas, and versioning.
- `agent_system.md` governs prompts, reporting, and the I/O layer, but does not replace the technical schema.

## Working Style

- Default: minimal-churn, narrow patch.
- Fix only what was requested, and do not clean up unrelated areas.
- If the task is explicitly limited to one node, do not expand scope into adjacent nodes.
- If semantic and formal contracts conflict in the same artifact, align both layers and do not leave two competing truths behind.
- If requiredness or a field type changes the schema contract, do not treat it as a minor editorial change.

## Default Guardrails

Without an explicit user request, the agent must not:
- create new artifact families or registry layers;
- redesign state-model, release, freshness, or decision-lifecycle nodes;
- change file-path or directory models;
- duplicate the full architecture inside `AGENTS.md`;
- rename existing documents for style alone.

## When to Stop and Escalate

The agent must stop and clearly state the problem if:
- the task would break a higher-priority document;
- a narrow patch is no longer enough and a broader redesign would be required;
- the work now depends on resolving an unlocked product rule, not just document consistency;
- it would need to change more files than the user allowed.

## Medical and Localization Discipline

- Do not guess Lithuanian medical terminology.
- If a term or localization decision is unclear, rely on LT / ES sources according to the project rules.
- The canonical LT chapter and the learning block must never be merged.

## Expected Response Format After Edits

Unless the user specifies otherwise, the agent should briefly report:
- which files were changed;
- what changed;
- what was intentionally left untouched;
- and, if useful, a short diff or grep evidence summary.

If the user provides a strict output format, follow that format instead of this default.
