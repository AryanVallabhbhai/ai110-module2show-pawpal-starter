"""Tests for the PawPal logic layer."""

import sys
from datetime import date
from pathlib import Path

# Allow importing pawpal_system.py from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Task


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
