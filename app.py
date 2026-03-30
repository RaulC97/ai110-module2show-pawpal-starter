import streamlit as st
from datetime import datetime
from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# --- Owner Setup ---
st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value="Raul")

if st.button("Set Owner"):
    st.session_state.owner = Owner(owner_name)
    st.session_state.scheduler = Scheduler(st.session_state.owner)
    st.success(f"Owner '{owner_name}' created.")

if st.session_state.owner is None:
    st.info("Set an owner above to get started.")
    st.stop()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Patch")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species)
    owner.add_pet(new_pet)
    st.success(f"{pet_name} the {species} added.")

if owner.pets:
    st.write("**Registered pets:**", ", ".join(p.name for p in owner.pets))

st.divider()

# --- Schedule a Task ---
st.subheader("Schedule a Task")

if not owner.pets:
    st.warning("Add at least one pet before scheduling tasks.")
else:
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_desc = st.text_input("Description", value="30 min walk around the park")
        task_pet = st.selectbox("Assign to pet", [p.name for p in owner.pets])
    with col2:
        task_priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH"], index=2)
        task_freq = st.selectbox("Frequency", ["ONCE", "DAILY", "WEEKLY"])
        task_time = st.time_input("Time", value=datetime.now().replace(second=0, microsecond=0))

    if st.button("Add Task"):
        pet = owner.get_pet(task_pet)
        task = Task(
            title=task_title,
            description=task_desc,
            time=datetime.combine(datetime.today(), task_time),
            priority=Priority[task_priority],
            frequency=Frequency[task_freq],
        )
        owner.create_task(pet, task)
        st.success(f"Task '{task_title}' added to {task_pet}.")

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    scheduler.generate()

if scheduler.scheduled_tasks:
    for task in scheduler.scheduled_tasks:
        pet_name_label = next(
            (p.name for p in owner.pets if task in p.tasks), "?"
        )
        status = "✅" if task.completed else "🕐"
        st.markdown(
            f"{status} **{task.time.strftime('%I:%M %p')}** — "
            f"{task.title} *({pet_name_label})* | "
            f"`{task.priority.name}` | `{task.frequency.value}`"
        )
        st.caption(f"   {task.description}")
else:
    st.info("Add tasks and click 'Generate Schedule' to see results.")
