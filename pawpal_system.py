"""PawPal system logic layer.

Backend classes for the pet care app: Owner, Pet, Task, Scheduler.
Skeleton generated from diagrams/uml_draft.mmd. Method bodies are stubs.
"""

from dataclasses import dataclass, field
from datetime import date


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
        pass

    def mark_incomplete(self) -> None:
        pass

    def is_overdue(self) -> bool:
        pass

    def reschedule(self, new_date: date) -> None:
        pass


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
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def list_tasks(self) -> list[Task]:
        pass

    def update_info(self, name: str, age: int) -> None:
        pass


@dataclass
class Owner:
    owner_id: int
    name: str
    email: str
    phone: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def list_pets(self) -> list[Pet]:
        pass

    def update_contact(self, email: str, phone: str) -> None:
        pass


@dataclass
class Scheduler:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_due_today(self) -> list[Task]:
        pass

    def get_overdue(self) -> list[Task]:
        pass

    def get_upcoming(self, days: int) -> list[Task]:
        pass

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        pass
