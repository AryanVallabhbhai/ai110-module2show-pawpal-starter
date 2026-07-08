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
