# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- **Sort by time** — tasks display in chronological (`HH:MM`) order via `Scheduler.sort_by_time()`.
- **Filter tasks** — narrow the task list by pet name and/or completion status via `Scheduler.filter_tasks()`.
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags any two tasks sharing a date + time slot (same or different pet) and surfaces a warning instead of crashing.
- **Daily / weekly recurrence** — completing a repeating task via `Scheduler.complete_task()` auto-spawns the next occurrence (`Task.next_due_date()` does the `timedelta` math).
- **Daily schedule view** — due-today, overdue count, and upcoming-7-days summary from the `Scheduler` query methods.
- **Owner ↔ Pet ↔ Task model** — bidirectional back-references keep relationships in sync on add/remove.

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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```text
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

## Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

**What the tests cover** (`tests/test_pawpal.py`):

- **Task basics** — `mark_done()` flips completion; `add_task()` grows the pet's task list.
- **Sorting correctness** — `sort_by_time()` returns out-of-order tasks in chronological (`HH:MM`) order.
- **Recurrence logic** — completing a `daily` task spawns a new task due the following day, on the same pet, still incomplete.
- **Conflict detection** — `detect_conflicts()` flags 2+ tasks sharing a date + time slot (even across different pets) and produces no false positives when times differ.

Successful test run:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\aBOSS\Documents\GitHub\ai110-module2show-pawpal-starter
plugins: anyio-4.11.0
collected 6 items

tests/test_pawpal.py::test_task_completion PASSED                        [ 16%]
tests/test_pawpal.py::test_task_addition PASSED                          [ 33%]
tests/test_pawpal.py::test_sort_by_time_chronological PASSED             [ 50%]
tests/test_pawpal.py::test_recurrence_creates_next_day_task PASSED       [ 66%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED [ 83%]
tests/test_pawpal.py::test_detect_conflicts_no_false_positive PASSED     [100%]

============================== 6 passed in 0.03s ==============================
```

### Confidence level: (4/5)

Core scheduling logic — sorting, recurrence, conflict detection — is covered and green.
Docked one star because tests don't yet exercise weekly recurrence, month/year date
rollover, empty-scheduler edge cases, or the Streamlit UI wiring in `app.py`.

## Smarter Scheduling

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

##  Demo Walkthrough

Run the Streamlit UI:

```bash
streamlit run app.py
```

### Main UI features

- **Owner** — edit the owner's name.
- **Add a Pet** — enter name, species, breed, age; the pet is registered with the scheduler so its tasks appear in queries.
- **Schedule a Task** — pick a pet, title, type, due date, **time**, and how it **repeats** (one-time / daily / weekly).
- **Conflict warnings** — any date + time clash is shown as a `st.warning` banner at the top of the schedule.
- **Today's Schedule** — due-today tasks sorted by time, plus Overdue and Upcoming (7d) metrics.
- **Mark a Task Done** — complete a task; recurring tasks auto-reschedule the next occurrence.
- **All Tasks** — filter by pet and status, displayed in time order.

### Example workflow

1. Add a pet (e.g. "Rex", dog).
2. Schedule a task — "Morning feed", feed, today, `07:00`, repeats **daily**.
3. Schedule a second task at the **same time** for another pet to trigger a conflict warning.
4. View **Today's Schedule** — tasks appear sorted by time; the conflict banner shows at the top.
5. Open **Mark a Task Done**, complete the daily "Morning feed" — a new instance is auto-scheduled for tomorrow.
6. Use **All Tasks** filters to view, e.g., only Rex's open tasks.

### Key Scheduler behaviors shown

- **Sorting** — schedule + all-tasks views are chronological (`sort_by_time()`).
- **Filtering** — the All Tasks pet/status dropdowns call `filter_tasks()`.
- **Conflict warnings** — same-slot tasks surface via `detect_conflicts()`.
- **Recurrence** — completing a daily/weekly task spawns the next occurrence via `complete_task()`.

### Sample CLI output (`python main.py`)

```text
========================================
  TODAY'S SCHEDULE - 2026-07-07
========================================
  [ walk] Evening walk  (Rex)
  [ feed] Morning feed  (Rex)
  [ walk] Bedtime walk  (Rex)
  [ meds] Night meds  (Mia)
----------------------------------------
  Overdue: 1   Upcoming (7d): 5
========================================

Conflict check:
  WARNING: 2 tasks clash at 2026-07-07 21:45: 'Bedtime walk' (Rex), 'Night meds' (Mia)

Recurring task automation:
  Before: 6 tasks
  Completed 'Morning feed' (daily, due 2026-07-07) -> new instance id=7 due 2026-07-08
  Completed 'Evening walk' (weekly, due 2026-07-07) -> new instance id=8 due 2026-07-14
  After:  8 tasks

Sorted by time:
  [x] 07:00  Morning feed   (Rex)
  [ ] 07:00  Morning feed   (Rex)
  [ ] 09:15  Vet checkup    (Rex)
  [ ] 12:00  Litter clean   (Mia)
  [x] 18:30  Evening walk   (Rex)
  [ ] 18:30  Evening walk   (Rex)
  [ ] 21:45  Bedtime walk   (Rex)
  [ ] 21:45  Night meds     (Mia)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
