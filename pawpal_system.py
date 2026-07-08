"""PawPal system logic layer.

Backend classes for the pet care app: Owner, Pet, Task, Scheduler.
Skeleton generated from diagrams/uml_draft.mmd. Method bodies are stubs.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    task_id: int
    title: str
    type: str  # feed / walk / vet / groom / meds
    due_date: date
    time: str = "00:00"  # "HH:MM" 24-hour clock time-of-day
    recurrence: str | None = None  # None = one-time
    completed: bool = False
    pet: "Pet | None" = None

    def mark_done(self) -> None:
        """Mark this task completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task not completed."""
        self.completed = False

    def is_overdue(self) -> bool:
        """Overdue = due before today and not yet completed."""
        return not self.completed and self.due_date < date.today()

    def reschedule(self, new_date: date) -> None:
        """Move this task to a new due date."""
        self.due_date = new_date

    def next_due_date(self) -> date | None:
        """Due date of the next occurrence, or None if one-time.

        timedelta does calendar-correct date math: adding a timedelta to a
        date rolls month/year boundaries automatically (e.g. Jan 31 + 1 day
        -> Feb 1), so no manual day/month handling is needed.
        """
        if self.recurrence == "daily":
            return self.due_date + timedelta(days=1)
        if self.recurrence == "weekly":
            return self.due_date + timedelta(weeks=1)
        return None  # one-time (None) or unknown recurrence


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    breed: str
    age: int
    owner: "Owner | None" = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach task to this pet and set back-reference."""
        if task not in self.tasks:
            self.tasks.append(task)
        task.pet = self

    def remove_task(self, task: Task) -> None:
        """Detach task from this pet and clear back-reference."""
        if task in self.tasks:
            self.tasks.remove(task)
        if task.pet is self:
            task.pet = None

    def list_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks

    def update_info(self, name: str, age: int) -> None:
        """Update this pet's name and age."""
        self.name = name
        self.age = age


@dataclass
class Owner:
    owner_id: int
    name: str
    email: str
    phone: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Attach pet to this owner and set back-reference."""
        if pet not in self.pets:
            self.pets.append(pet)
        pet.owner = self

    def remove_pet(self, pet: Pet) -> None:
        """Detach pet from this owner and clear back-reference."""
        if pet in self.pets:
            self.pets.remove(pet)
        if pet.owner is self:
            pet.owner = None

    def list_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        return self.pets

    def update_contact(self, email: str, phone: str) -> None:
        """Update this owner's email and phone."""
        self.email = email
        self.phone = phone


@dataclass
class Scheduler:
    """Query brain. Owns no tasks — tasks live in pet.tasks.

    Holds a pet registry so query methods can scan across all pets.
    """

    pets: list[Pet] = field(default_factory=list)

    def register_pet(self, pet: Pet) -> None:
        """Add pet to registry so its tasks appear in queries."""
        if pet not in self.pets:
            self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Flatten every task across registered pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def _next_task_id(self) -> int:
        """One past the highest task_id in the registry (1 if empty)."""
        ids = [t.task_id for t in self.all_tasks()]
        return max(ids) + 1 if ids else 1

    def complete_task(self, task: Task) -> Task | None:
        """Mark task done; if recurring, spawn + attach the next occurrence.

        Returns the newly created follow-up Task, or None for one-time tasks.
        The new instance keeps the same title/type/time/recurrence and the
        same pet, but gets a fresh id, the next due_date, and completed=False.
        """
        task.mark_done()
        next_due = task.next_due_date()
        if next_due is None:
            return None  # one-time task: nothing to spawn

        follow_up = Task(
            task_id=self._next_task_id(),
            title=task.title,
            type=task.type,
            due_date=next_due,
            time=task.time,
            recurrence=task.recurrence,
        )
        if task.pet is not None:
            task.pet.add_task(follow_up)  # sets back-ref; pet already registered
        return follow_up

    def get_due_today(self) -> list[Task]:
        """Incomplete tasks due exactly today."""
        today = date.today()
        return [t for t in self.all_tasks() if not t.completed and t.due_date == today]

    def get_overdue(self) -> list[Task]:
        """Incomplete tasks past their due date."""
        return [t for t in self.all_tasks() if t.is_overdue()]

    def get_upcoming(self, days: int) -> list[Task]:
        """Incomplete tasks due from today through today + days."""
        today = date.today()
        end = today + timedelta(days=days)
        return [
            t for t in self.all_tasks()
            if not t.completed and today <= t.due_date <= end
        ]

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return a copy of the given pet's task list."""
        return list(pet.tasks)

    def detect_conflicts(self) -> list[str]:
        """Find tasks scheduled at the same date + time; return warnings.

        Lightweight strategy: bucket every incomplete task by its
        (due_date, time) slot in a dict. Any slot holding 2+ tasks is a
        conflict. Returns a list of human-readable warning strings — empty
        list means no conflicts. Never raises, so the caller can print and
        keep running.
        """
        slots: dict[tuple[date, str], list[Task]] = {}
        for t in self.all_tasks():
            if t.completed:
                continue  # done tasks can't clash
            slots.setdefault((t.due_date, t.time), []).append(t)

        warnings: list[str] = []
        for (due, time), tasks in slots.items():
            if len(tasks) < 2:
                continue
            labels = ", ".join(
                f"'{t.title}' ({t.pet.name if t.pet else '?'})" for t in tasks
            )
            warnings.append(f"WARNING: {len(tasks)} tasks clash at {due} {time}: {labels}")
        return warnings

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Return tasks sorted by time-of-day (ascending).

        Uses sorted() with a lambda key on the "HH:MM" string. Zero-padded
        24-hour strings sort correctly lexicographically ("09:00" < "10:30"),
        so no time parsing is needed. Defaults to all registered tasks.
        """
        if tasks is None:
            tasks = self.all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter tasks by completion status and/or pet name.

        Pass `completed` (True/False) to match that status, and/or `pet_name`
        to match a pet by name. Unset (None) filters are ignored. With no
        filters, returns every task.
        """
        tasks = self.all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet is not None and t.pet.name == pet_name]
        return tasks
