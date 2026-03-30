# PawPal+ (Module 2 Project)

## Features

### Multi-key Sorting
Tasks are sorted by two keys: scheduled time (ascending) and priority (descending) as a tiebreaker. When two tasks share the same time slot, the higher-priority task always appears first. Implemented in `Scheduler.generate()` and `Scheduler.sort_by_time()` using Python's `sorted()` with a compound tuple key `(task.time, -task.priority.value)`.

### Recurring Task Scheduling
Tasks can repeat on a `DAILY` (+1 day) or `WEEKLY` (+7 days) cadence. When a recurring task is marked complete, `Task.next_occurrence()` creates a new `Task` instance at the next due time — preserving the original title, description, priority, and frequency — and adds it back to the pet's task list. The schedule is regenerated automatically so the new occurrence appears immediately.

### Conflict Detection
`Scheduler.get_conflicts()` groups all pending tasks by their exact `datetime` across every pet. Any time slot that has two or more pending tasks triggers a warning string that names each conflicting task and its pet. Completed tasks are excluded so resolved conflicts do not keep appearing.

### Completion Status Filtering
`Scheduler.filter_tasks()` accepts optional `completed` and `pet_name` parameters and composes them independently. Passing `completed=False` returns only pending tasks; `pet_name="Bella"` narrows results to one pet; both together intersect the two filters. The method operates on `scheduled_tasks` so sort order is always preserved.

### Owner-scoped Task Assignment
`Owner.create_task()` enforces that a task can only be assigned to a pet that belongs to that owner, raising `ValueError` for unrecognized pets. Tasks live on the `Pet`, not the `Owner`, so each pet carries its own independent task list and pending/completed views via `Pet.get_pending_tasks()` and `Pet.get_completed_tasks()`.



You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


# Testing PawPal+

cd tests then run python -m pytest

In these test, we test creating tasks, adding pets, making owner with pits. Next is testing
the sorting of the scheduler, which task comes up first if the time is the same. Testing
recurring logic.