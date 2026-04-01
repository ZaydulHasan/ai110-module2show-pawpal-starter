# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design included four classes: `Task`, `Pet`, `Owner`, and `Scheduler`. I assigned responsibilities as follows:
- `Task` holds a single care activity — its description, scheduled time, frequency, priority, and completion status.
- `Pet` stores a pet's basic info (name, species, age) and owns a list of tasks.
- `Owner` manages multiple pets and provides a single method to retrieve all tasks across every pet.
- `Scheduler` is the "brain" — it takes an owner and handles sorting, filtering, conflict detection, and recurring task logic.

I used Python dataclasses for `Task`, `Pet`, and `Owner` to keep the code clean and avoid writing boilerplate `__init__` methods manually.

**b. Design changes**

Yes, the design changed during implementation. Originally I planned for `predict_label` to return a "mixed" label when the score was ±1, but this caused nearly every post to be classified as mixed since most short posts only trigger one sentiment word. I changed the thresholds so that any score above 0 returns "positive" and any score below 0 returns "negative." This made the rule-based classifier much more useful in practice, even though it loses some nuance for genuinely ambiguous posts.

For PawPal+, I also added a `due_date` field to `Task` after realizing that recurring task logic (daily/weekly rescheduling) required knowing when the original task was due. This wasn't in the initial UML but was necessary for the recurrence feature to work correctly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: time (tasks are sorted chronologically by their HH:MM field) and conflict detection (two tasks at the same time trigger a warning). Priority is stored on each task and displayed in the UI, but the current scheduler sorts by time rather than priority — meaning a "low" priority task at 07:00 appears before a "high" priority task at 09:00.

I chose time-based sorting as the primary constraint because a daily care schedule is fundamentally time-driven — a pet needs to be fed at 7:30am regardless of how that task ranks in priority.

**b. Tradeoffs**

The main tradeoff is that conflict detection only checks for exact time matches, not overlapping durations. For example, a 30-minute walk starting at 09:00 and a 5-minute medication also at 09:15 would not be flagged as a conflict, even though they overlap in real life. This is a reasonable simplification for a prototype — tasks don't have a duration field, and adding one would significantly complicate the scheduling logic. Documenting this as a known limitation is more honest than pretending it doesn't exist.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project for several purposes: generating the initial class skeletons from a description of the system, implementing the scoring and negation logic in `mood_analyzer.py`, writing the pytest test suite, and connecting the backend to the Streamlit UI. The most helpful prompts were specific and task-focused — for example, "implement a method that sorts Task objects by their HH:MM time string" produced better results than vague requests like "make the scheduler smarter."

**b. Judgment and verification**

One example where I did not accept the AI suggestion as-is was the threshold logic in `predict_label`. The AI initially suggested using ±2 thresholds, which caused nearly every post to be classified as "mixed" because single-word posts only score ±1. I noticed this by running the program and checking the actual output — the accuracy was only 43%. I overrode the suggestion and changed the thresholds to ±1, which raised accuracy to 64%. This showed that AI-generated logic still needs to be validated against real data, not just accepted because it looks reasonable in isolation.

---

## 4. Testing and Verification

**a. What you tested**

I wrote six automated tests covering the most critical behaviors:
- `test_mark_complete_changes_status` — verifies that calling `mark_complete()` actually flips the completed flag
- `test_add_task_increases_count` — verifies that `add_task()` increases the pet's task count
- `test_sort_by_time` — verifies that the scheduler returns tasks in chronological order
- `test_daily_recurrence` — verifies that completing a daily task creates a new task for the next day
- `test_conflict_detection` — verifies that two tasks at the same time generate a warning
- `test_no_false_conflicts` — verifies that tasks at different times do not generate false warnings

These tests matter because they cover the three algorithmic features (sorting, recurrence, conflict detection) that are most likely to break silently — a bug in any one of them could produce wrong output with no error message.

**b. Confidence**

All 6 tests pass, so I am fairly confident the core logic is correct for standard cases. Edge cases I would test next include: a pet with zero tasks, completing a "once" task (should not create a new task), adding two pets with tasks at identical times across different pets, and a weekly task recurring correctly after 7 days.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the backend architecture in `pawpal_system.py`. The four classes have clear, single responsibilities and interact cleanly — `Scheduler` only needs an `Owner` reference to access everything, and `Owner.get_all_tasks()` acts as a clean aggregation point. The design made it easy to add features (like conflict detection) without touching unrelated code.

**b. What you would improve**

If I had another iteration, I would add data persistence so pets and tasks survive between app restarts — right now all data is lost when the Streamlit session ends. I would also add a "duration" field to `Task` so conflict detection could catch overlapping tasks rather than just exact time matches. Finally, I would separate the test data from the main data more clearly, so tests don't depend on specific hardcoded values.

**c. Key takeaway**

The most important thing I learned is that AI is most useful as a first-draft generator, not a final decision-maker. It saved significant time on boilerplate and repetitive code, but the decisions that actually determined whether the system worked well — like the scoring thresholds, the choice to sort by time over priority, or the conflict detection strategy — all required human judgment based on running the system and observing its actual behavior. AI accelerates building; it doesn't replace thinking.