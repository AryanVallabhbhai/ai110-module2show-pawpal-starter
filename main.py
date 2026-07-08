"""PawPal testing ground.

Builds a sample owner, pets, and tasks, then prints today's schedule.
Run: python main.py
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # --- Owner ---
    owner = Owner(owner_id=1, name="Alex", email="alex@example.com", phone="555-0100")

    # --- Pets ---
    rex = Pet(pet_id=1, name="Rex", species="dog", breed="Labrador", age=3)
    mia = Pet(pet_id=2, name="Mia", species="cat", breed="Siamese", age=2)
    owner.add_pet(rex)
    owner.add_pet(mia)

    # --- Tasks (different times) ---
    today = date.today()
    t1 = Task(task_id=1, title="Morning feed", type="feed", due_date=today)
    t2 = Task(task_id=2, title="Evening walk", type="walk", due_date=today)
    t3 = Task(task_id=3, title="Vet checkup", type="vet", due_date=today + timedelta(days=3))
    t4 = Task(task_id=4, title="Litter clean", type="groom", due_date=today - timedelta(days=1))

    rex.add_task(t1)
    rex.add_task(t3)
    mia.add_task(t2)
    mia.add_task(t4)

    # --- Scheduler ---
    scheduler = Scheduler()
    scheduler.register_pet(rex)
    scheduler.register_pet(mia)

    # --- Today's Schedule ---
    print("=" * 40)
    print(f"  TODAY'S SCHEDULE - {today.isoformat()}")
    print("=" * 40)

    due_today = scheduler.get_due_today()
    if not due_today:
        print("  Nothing due today.")
    else:
        for task in due_today:
            pet_name = task.pet.name if task.pet else "?"
            print(f"  [{task.type:>5}] {task.title}  ({pet_name})")

    print("-" * 40)
    print(f"  Overdue: {len(scheduler.get_overdue())}   "
          f"Upcoming (7d): {len(scheduler.get_upcoming(7))}")
    print("=" * 40)


if __name__ == "__main__":
    main()
