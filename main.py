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

    # --- Tasks (added OUT OF ORDER by time on purpose) ---
    today = date.today()
    t1 = Task(task_id=1, title="Morning feed", type="feed", due_date=today, time="07:00", recurrence="daily")
    t2 = Task(task_id=2, title="Evening walk", type="walk", due_date=today, time="18:30", recurrence="weekly")
    t3 = Task(task_id=3, title="Vet checkup", type="vet", due_date=today + timedelta(days=3), time="09:15")
    t4 = Task(task_id=4, title="Litter clean", type="groom", due_date=today - timedelta(days=1), time="12:00")
    t5 = Task(task_id=5, title="Night meds", type="meds", due_date=today, time="21:45")
    # t6 clashes with t5: same date + time, different pet.
    t6 = Task(task_id=6, title="Bedtime walk", type="walk", due_date=today, time="21:45")

    # Insertion order is deliberately not sorted by time.
    rex.add_task(t2)  # 18:30
    rex.add_task(t1)  # 07:00
    rex.add_task(t3)  # 09:15
    rex.add_task(t6)  # 21:45  <- conflicts with t5
    mia.add_task(t5)  # 21:45
    mia.add_task(t4)  # 12:00

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

    def show(label: str, tasks: list[Task]) -> None:
        print(f"\n{label}")
        if not tasks:
            print("  (none)")
            return
        for task in tasks:
            pet_name = task.pet.name if task.pet else "?"
            mark = "x" if task.completed else " "
            print(f"  [{mark}] {task.time}  {task.title:<14} ({pet_name})")

    # --- Conflict detection: tasks sharing a date + time slot ---
    print("\nConflict check:")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts.")

    # --- Recurring: completing a recurring task spawns its next occurrence ---
    print("\nRecurring task automation:")
    print(f"  Before: {len(scheduler.all_tasks())} tasks")
    spawn1 = scheduler.complete_task(t1)  # daily  -> +1 day
    spawn2 = scheduler.complete_task(t2)  # weekly -> +7 days
    for original, spawn in ((t1, spawn1), (t2, spawn2)):
        print(
            f"  Completed '{original.title}' ({original.recurrence}, due {original.due_date}) "
            f"-> new instance id={spawn.task_id} due {spawn.due_date}"
        )
    print(f"  After:  {len(scheduler.all_tasks())} tasks")

    # --- Sorting: by time-of-day ("HH:MM") ---
    show("Insertion order (all tasks):", scheduler.all_tasks())
    show("Sorted by time:", scheduler.sort_by_time())

    # --- Filtering: by completion status, then by pet name ---
    show("Filter completed=True:", scheduler.filter_tasks(completed=True))
    show("Filter completed=False:", scheduler.filter_tasks(completed=False))
    show("Filter pet_name='Rex':", scheduler.filter_tasks(pet_name="Rex"))

    # --- Combine filter + sort ---
    show(
        "Rex, incomplete, sorted by time:",
        scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Rex", completed=False)),
    )
    print("=" * 40)


if __name__ == "__main__":
    main()
