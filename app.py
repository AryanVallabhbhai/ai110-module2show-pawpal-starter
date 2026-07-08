import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This app wires the Streamlit UI to the backend logic layer in `pawpal_system.py`.
"""
)

# ---------------------------------------------------------------------------
# Application "memory".
#
# Streamlit reruns this whole script top-to-bottom on every interaction, so any
# plain local object would be recreated (empty) each run. st.session_state is a
# dict-like vault that persists across reruns. We build the Owner + Scheduler
# ONCE (guarded by the `not in` check) and reuse them afterwards.
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id=1, name="Jordan", email="jordan@example.com", phone="555-0100"
    )
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
# Counters for unique IDs (also survive reruns via session_state).
if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1
if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.divider()

# ---------------------------------------------------------------------------
# Owner info
# ---------------------------------------------------------------------------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# ---------------------------------------------------------------------------
# Add a Pet  ->  Owner.add_pet(...)  +  Scheduler.register_pet(...)
# ---------------------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="mixed")
    age = st.number_input("Age", min_value=0, max_value=40, value=2)
    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet and pet_name:
    pet = Pet(
        pet_id=st.session_state.next_pet_id,
        name=pet_name,
        species=species,
        breed=breed,
        age=int(age),
    )
    owner.add_pet(pet)          # logic-layer method sets pet.owner back-ref
    scheduler.register_pet(pet)  # so scheduler queries see this pet's tasks
    st.session_state.next_pet_id += 1
    st.success(f"Added {pet.name}.")

pets = owner.list_pets()
if not pets:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Schedule a Task  ->  Pet.add_task(...)
# ---------------------------------------------------------------------------
st.subheader("Schedule a Task")
if pets:
    with st.form("add_task_form", clear_on_submit=True):
        # Map each pet name back to its object for the selectbox.
        pet_by_name = {p.name: p for p in pets}
        chosen_pet_name = st.selectbox("For which pet?", list(pet_by_name.keys()))
        task_title = st.text_input("Task title", value="Morning walk")
        task_type = st.selectbox("Type", ["feed", "walk", "vet", "groom", "meds"])
        due = st.date_input("Due date", value=date.today())
        submitted_task = st.form_submit_button("Add task")

    if submitted_task and task_title:
        task = Task(
            task_id=st.session_state.next_task_id,
            title=task_title,
            type=task_type,
            due_date=due,
        )
        pet_by_name[chosen_pet_name].add_task(task)  # logic-layer method
        st.session_state.next_task_id += 1
        st.success(f"Added '{task.title}' for {chosen_pet_name}.")
else:
    st.caption("Add a pet first, then you can schedule tasks.")

st.divider()

# ---------------------------------------------------------------------------
# Today's Schedule  ->  Scheduler queries
# ---------------------------------------------------------------------------
st.subheader("Today's Schedule")

due_today = scheduler.get_due_today()
overdue = scheduler.get_overdue()
upcoming = scheduler.get_upcoming(7)

if due_today:
    st.write("**Due today**")
    st.table(
        [
            {"pet": t.pet.name if t.pet else "?", "task": t.title, "type": t.type}
            for t in due_today
        ]
    )
else:
    st.info("Nothing due today.")

col_a, col_b = st.columns(2)
col_a.metric("Overdue", len(overdue))
col_b.metric("Upcoming (7d)", len(upcoming))

with st.expander("All tasks"):
    all_tasks = scheduler.all_tasks()
    if all_tasks:
        st.table(
            [
                {
                    "pet": t.pet.name if t.pet else "?",
                    "task": t.title,
                    "type": t.type,
                    "due": t.due_date.isoformat(),
                    "done": t.completed,
                }
                for t in all_tasks
            ]
        )
    else:
        st.caption("No tasks yet.")
