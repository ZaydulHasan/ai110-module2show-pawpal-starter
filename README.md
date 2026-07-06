# PawPal+ (Module 2 Project)

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


## Sample Output

Add a real terminal example here after running `python main.py` locally. Paste the output that shows an owner being created, a pet being added, a few tasks being scheduled, and the final sorted schedule (including any conflict warnings).

## Testing PawPal+

The `tests/` folder covers the core `Scheduler` behaviors: sorting tasks by time, filtering by status and by pet, detecting time conflicts between tasks, and completing tasks (including recurring ones). Run the suite locally with the command below, then paste the real result here, for example six passed in zero point one two seconds.

```bash
pytest
```

## Smarter Scheduling

The table below maps each smarter scheduling feature to the method(s) that implement it in `pawpal_system.py`.

| Feature | Method(s) | Notes |
| --- | --- | --- |
| Task sorting | `Scheduler.sort_by_time()` | Returns every task for the owner ordered by scheduled time. |
| Filtering | `Scheduler.filter_by_status()`, `Scheduler.filter_by_pet()` | Lets the UI narrow tasks down to a single pet or completion status. |
| Conflict handling | `Scheduler.get_conflicts()` | Flags tasks across different pets scheduled at the same time so the owner can reschedule. |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.complete_task()` | Marks a task done and, for recurring tasks, automatically creates the next occurrence. |

## Demo Walkthrough

A typical run through the app follows four steps. First, the owner enters their name to set up their profile. Second, they add one or more pets with basic info such as name, species, and age. Third, for each pet they add care tasks with a description, scheduled time, priority, and frequency (one time, daily, or weekly). Finally, they generate the schedule, which displays every task sorted by time, highlights any time conflicts between pets, and lets the owner mark tasks complete as the day goes on.
