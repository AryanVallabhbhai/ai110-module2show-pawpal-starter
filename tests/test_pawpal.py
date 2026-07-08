"""Tests for the PawPal logic layer."""

import sys
from datetime import date, timedelta
from pathlib import Path

# Allow importing pawpal_system.py from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Scheduler, Task


def test_task_completion():
    """mark_done() flips completed status from False to True."""
    task = Task(task_id=1, title="Feed", type="feed", due_date=date.today())
    assert task.completed is False

    task.mark_done()

    assert task.completed is True


def test_task_addition():
    """Adding a task to a pet increases its task count by one."""
    pet = Pet(pet_id=1, name="Rex", species="dog", breed="Lab", age=3)
    assert len(pet.tasks) == 0

    task = Task(task_id=1, title="Walk", type="walk", due_date=date.today())
    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sort_by_time_chronological():
    """sort_by_time() returns tasks ordered by time-of-day, ascending.

    Tasks are added OUT OF ORDER; the returned list must be chronological.
    """
    pet = Pet(pet_id=1, name="Rex", species="dog", breed="Lab", age=3)
    today = date.today()
    pet.add_task(Task(1, "Evening", "walk", today, time="18:30"))
    pet.add_task(Task(2, "Morning", "feed", today, time="07:00"))
    pet.add_task(Task(3, "Midday", "meds", today, time="12:15"))

    scheduler = Scheduler()
    scheduler.register_pet(pet)

    times = [t.time for t in scheduler.sort_by_time()]
    assert times == ["07:00", "12:15", "18:30"]


def test_recurrence_creates_next_day_task():
    """Completing a daily task spawns a new task due the following day.

    complete_task() marks the original done and returns a fresh instance
    with due_date = original + 1 day, still incomplete, on the same pet.
    """
    pet = Pet(pet_id=1, name="Rex", species="dog", breed="Lab", age=3)
    today = date.today()
    original = Task(1, "Morning feed", "feed", today, time="07:00", recurrence="daily")
    pet.add_task(original)

    scheduler = Scheduler()
    scheduler.register_pet(pet)

    spawn = scheduler.complete_task(original)

    assert original.completed is True          # original marked done
    assert spawn is not None                   # a follow-up was created
    assert spawn.completed is False            # follow-up starts incomplete
    assert spawn.due_date == today + timedelta(days=1)  # next day
    assert spawn in pet.tasks                  # attached to same pet
    assert len(pet.tasks) == 2                 # original + spawn


def test_detect_conflicts_flags_duplicate_times():
    """detect_conflicts() warns when 2+ tasks share a date + time slot."""
    rex = Pet(pet_id=1, name="Rex", species="dog", breed="Lab", age=3)
    mia = Pet(pet_id=2, name="Mia", species="cat", breed="Siamese", age=2)
    today = date.today()
    # Same date + time, different pets -> should clash.
    rex.add_task(Task(1, "Walk", "walk", today, time="21:45"))
    mia.add_task(Task(2, "Meds", "meds", today, time="21:45"))
    # A non-clashing task at a different time.
    rex.add_task(Task(3, "Feed", "feed", today, time="07:00"))

    scheduler = Scheduler()
    scheduler.register_pet(rex)
    scheduler.register_pet(mia)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1        # exactly one clashing slot
    assert "21:45" in warnings[0]    # names the conflicting time


def test_detect_conflicts_no_false_positive():
    """No warnings when every task is at a distinct time."""
    pet = Pet(pet_id=1, name="Rex", species="dog", breed="Lab", age=3)
    today = date.today()
    pet.add_task(Task(1, "Feed", "feed", today, time="07:00"))
    pet.add_task(Task(2, "Walk", "walk", today, time="18:30"))

    scheduler = Scheduler()
    scheduler.register_pet(pet)

    assert scheduler.detect_conflicts() == []
