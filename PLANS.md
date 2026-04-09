# ExecPlans

This file adapts the OpenAI Cookbook `codex_exec_plans` pattern to this repo. It defines how to write and execute an ExecPlan so that a single stateless agent, or a human with no prior context, can understand the work from scratch and complete it safely.

This repo is currently a documentation and architecture source of truth, not a typical application codebase. Because of that, ExecPlans here must cover not only code implementation, but also normative documents, artifact contracts, semantic and formal consistency, and schema-level reasoning.

## How to Use ExecPlans in This Repo

When creating an ExecPlan:
- keep it fully self-contained;
- assume the reader is a beginner who only has the current working tree and the plan itself;
- do not rely on earlier plans, chat history, or unwritten assumptions;
- include all context needed to perform the work safely.

When executing an ExecPlan:
- carry it through from design to implementation;
- do not hand "next steps" back to the user after every milestone unless there is a real blocker;
- update the living sections at every stopping point;
- if new facts or decisions appear during the work, reflect them in the plan, not only in the final message.

When revising an existing ExecPlan:
- update all affected sections, not just one line;
- leave a short revision note at the bottom explaining what changed and why.

## Non-Negotiable Requirements

- Every ExecPlan must be fully self-contained.
- Every ExecPlan must be a living document.
- Every ExecPlan must allow a beginner to complete the work end-to-end without prior knowledge of the repo.
- Every ExecPlan must aim at an observable result, not just "change files".
- Every non-trivial term must be defined in plain language or not used.
- The plan must clearly state what the user will be able to do or verify after the change.

## Repo-Specific Orientation

Document priority in this repo is:
1. `project_constitution.md`
2. `product_spec.md`
3. `architecture.md`
4. `agent_system.md`
5. `implementation_plan.md`
6. `validation_plan.md`
7. `open_questions.md`

`reference_examples.md` is a helper reference layer only.

If a plan touches normative documents, it must clearly state:
- which rule belongs to the product layer;
- which rule belongs to technical architecture;
- which part is only an agent reporting / I-O layer;
- how conflicts are resolved by document priority.

If a plan touches an artifact contract and the repo has both a semantic artifact description and a formal schema contract, the plan must address both layers. It is not acceptable to fix only one and leave two competing truths behind.

## When an ExecPlan Is Required

An ExecPlan is required when the task:
- crosses more than one file or more than one architectural node;
- changes artifact semantics, requiredness, schemas, or versioning consequences;
- requires meaningful research or multiple steps;
- has enough context that a later session would get lost without a self-contained plan;
- is larger than one truly small, local correction.

An ExecPlan is not required only when the task is genuinely small, local, and does not need broader context.

## Formatting

If an ExecPlan is written as a standalone `.md` file, the file itself should contain one complete plan without extra outer fenced code blocks.

If an ExecPlan is written in chat, it should appear in one fenced `md` block. Inside that block, do not use additional triple-backtick fences. Show commands, transcripts, diffs, and snippets as indented examples.

Write prose first. Checklists are allowed only in the `Progress` section, where they are required. Avoid tables when they add formality without clarity.

## Repo-Specific Guidance

### 1. Self-Contained Context

The plan must not say "as described in the architecture document" and stop there. If the task depends on understanding:
- what `chapter_pack` is;
- how a semantic artifact description differs from a formal schema;
- why `agent_system.md` must not become a technical schema duplicate;
- how this repo interprets a "breaking change";

the plan must explain that context directly, in its own words, with exact repo-relative paths for the files that must be read or edited.

### 2. Scope Boundaries Must Be Explicit

Every ExecPlan must include a clear scope lock. If the user limited:
- allowed files;
- allowed tasks;
- forbidden areas;
- nodes that must not be touched;

the plan must restate those limits directly. Do not leave them implicit. If something is intentionally left untouched, say so explicitly.

### 3. Validation in This Repo Is Not Always Runtime Testing

Because this repo is a source of truth for documents and artifact contracts, validation may take the form of:
- `rg` or `grep` evidence that the same required field appears in both layers;
- diff evidence that semantic and formal descriptions no longer conflict;
- file-reading evidence that `optional` and `required` classifications now align;
- and, if code or tests are added later, then real test commands as well.

If the work is document-only, the plan must not pretend there is runtime validation when the repo does not have it. Instead, it must describe exactly how consistency will be proven.

### 4. Medical and Localization Discipline

If the plan touches:
- Lithuanian medical terminology;
- LT / ES localization decisions;
- claim support logic;
- high-risk clinical semantics;

the plan must explicitly say how guessing will be avoided and which sources or repo rules will govern the decision.

### 5. Filenames and Paths

Use real repo-relative paths with the actual filenames on disk. Most files in this repo are lowercase; `PLANS.md` is an intentional exception.

## Required ExecPlan Sections

Every ExecPlan in this repo must contain these sections:

## Purpose / Big Picture

Briefly explain what changes for the user or repo operator and how it will be verified. If the change is document-only, say which consistency or execution conflict will disappear after the change.

## Scope Boundaries

Explicitly list:
- which files may be edited;
- which files or nodes must not be touched;
- what is intentionally left out of scope.

## Progress

Use a checkbox list with timestamps. Every stopping point must be recorded.

Example:
- [x] (2026-04-08 12:10Z) Read `product_spec.md` and `architecture.md`; identified a conflict between the semantic and formal `chapter_pack` contract.
- [ ] Fix the semantic `claims/<slug>.yaml` description.
- [ ] Gather `rg` evidence after the change.

## Surprises & Discoveries

Record unexpected findings.

Example:
- Observation: The semantic `claims` description required `chapter_slug` at the item level, while the formal schema treated it as a top-level field.
  Evidence: Semantic section in `architecture.md` and the `schema_type: claims_register` required list.

## Decision Log

Every meaningful decision must be recorded:
- Decision: ...
  Rationale: ...
  Date/Author: ...

## Outcomes & Retrospective

At completion, or after a major milestone, record:
- what was achieved;
- what remains undone;
- what was learned;
- whether the result matches the Purpose / Big Picture.

## Context and Orientation

Describe the current state as if the reader knows nothing about this repo. Name the key files using full repo-relative paths. If you use a term such as "semantic contract", "formal schema", or "learning-block planning-state", define it immediately in plain language.

## Canonical Source Mapping

This repo requires this extra section. It must state directly:
- which rule comes from `product_spec.md`;
- which rule must be implemented in `architecture.md`;
- which place is only the reporting layer in `agent_system.md`;
- and, if there is a conflict, which document wins and why.

## Milestones

If the work is large, break it into independently verifiable milestones. Each milestone must briefly say:
- what will be changed;
- what new result will exist at the end of the milestone;
- how that result will be checked.

Milestones should be narrative, not just numbered stubs.

## Plan of Work

Describe the concrete sequence of edits. For each edit, name:
- the file;
- the location inside the file;
- what will be changed;
- why that edit is needed.

If an artifact contract has both a semantic and a formal layer, show clearly how both will be aligned.

## Concrete Steps

Give exact commands and the working directory.

Example:
    cwd: /Users/dzukauskas/Desktop/EPUB project copy
    sed -n '350,430p' architecture.md

    cwd: /Users/dzukauskas/Desktop/EPUB project copy
    rg -n "required_claims|supporting_lt_sources" architecture.md

If a command should produce evidence, show a short expected transcript.

## Validation and Acceptance

Explain how the result will be checked. In this repo, validation is often behavior plus consistency evidence.

Examples:
- after the change, `rg` should show that the same field exists in both the semantic and formal artifact descriptions;
- after the change, `notes` is no longer in the required claim-item list but still appears under `Optional` in the formal schema;
- if the work includes code, provide the real test commands and what they should show.

## Idempotence and Recovery

Explain which steps are safe to repeat. If a step is risky, describe a safe retry or rollback path. If the work is document-only, say so directly.

## Artifacts and Notes

Include the most important evidence:
- short diff excerpts;
- `rg` or `grep` output snippets;
- short transcripts.

Keep them concise and focused on what proves success.

## Interfaces and Dependencies

If the work touches code, name modules, functions, types, and libraries.

If the work is document-oriented, this section should name:
- which artifact types are affected;
- which fields are required or optional;
- which documents or sections depend on one another;
- which new competing truth sources must not be created.

## Revision Note

Every meaningful plan revision must end with a short note:
- what changed in the plan;
- why it changed.

## Short ExecPlan Stub for This Repo

Use this as a starting shape:

# <Short, action-oriented title>

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. This file must be maintained in accordance with `PLANS.md`.

## Purpose / Big Picture

## Scope Boundaries

## Progress

- [ ] (YYYY-MM-DD HH:MMZ) ...

## Surprises & Discoveries

- Observation: ...
  Evidence: ...

## Decision Log

- Decision: ...
  Rationale: ...
  Date/Author: ...

## Outcomes & Retrospective

## Context and Orientation

## Canonical Source Mapping

## Milestones

## Plan of Work

## Concrete Steps

## Validation and Acceptance

## Idempotence and Recovery

## Artifacts and Notes

## Interfaces and Dependencies

## Revision Note

## Final Rule

An ExecPlan is only good if a new agent can use it to:
- understand the problem without extra explanation;
- know which files to read and edit;
- see how success will be proven;
- resume after a pause without chat history;
- avoid creating a new competing truth inside the repo.
