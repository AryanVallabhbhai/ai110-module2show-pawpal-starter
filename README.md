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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
========================================
  TODAY'S SCHEDULE - 2026-07-07
========================================
  [ feed] Morning feed  (Rex)
  [ walk] Evening walk  (Mia)
----------------------------------------
  Overdue: 1   Upcoming (7d): 3
========================================
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

All scheduling logic lives in the `Scheduler` class in `pawpal_system.py` (recurrence math also uses `Task.next_due_date()`).

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by time-of-day, ascending |
| Filtering | `Scheduler.filter_tasks()` | By pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Same date + time = clash, returns warnings |
| Recurring tasks | `Scheduler.complete_task()`, `Task.next_due_date()` | Daily/weekly auto-respawn on complete |

### Sorting — `Scheduler.sort_by_time()`

Returns tasks ordered by time-of-day (ascending). Uses `sorted()` with a lambda
key on the `"HH:MM"` string. Zero-padded 24-hour strings sort correctly
lexicographically (`"09:00" < "10:30"`), so no time parsing is needed. Defaults
to all registered tasks; pass a list to sort a subset (e.g. combine with a filter).

### Filtering — `Scheduler.filter_tasks()`

Filters tasks by `completed` status (True/False) and/or `pet_name`. Each filter is
optional — an unset (`None`) filter is ignored, so calling with no args returns
every task. Filters compose (e.g. `pet_name="Rex", completed=False`).

### Conflict detection — `Scheduler.detect_conflicts()`

Lightweight strategy: buckets every incomplete task by its `(due_date, time)` slot
in a dict. Any slot holding 2+ tasks is a conflict — across the same pet or
different pets. Returns a list of human-readable warning strings (empty = no
conflicts). Never raises, so the caller prints the warning and keeps running.
Tradeoff: matches exact time slots only (no task-duration overlap).

### Recurring tasks — `Scheduler.complete_task()` + `Task.next_due_date()`

When a `"daily"` or `"weekly"` task is completed via `complete_task()`, it is marked
done and a fresh instance is auto-created for the next occurrence and attached to the
same pet. `Task.next_due_date()` computes the next date with `timedelta`
(daily → `+timedelta(days=1)`, weekly → `+timedelta(weeks=1)`), which handles
month/year rollover correctly. One-time tasks (`recurrence=None`) spawn nothing.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
