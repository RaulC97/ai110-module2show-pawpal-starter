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
        scheduler.generate()
        st.success(f"Task '{task_title}' added to {task_pet}.")

st.divider()

# --- Conflict Warnings ---
conflicts = scheduler.get_conflicts()
if conflicts:
    st.subheader("⚠️ Schedule Conflicts")
    for msg in conflicts:
        st.warning(msg)

# --- Generate Schedule ---
st.subheader("Today's Schedule")

col_gen, col_filter = st.columns([1, 2])
with col_gen:
    if st.button("Generate Schedule"):
        scheduler.generate()

with col_filter:
    pet_filter_options = ["All pets"] + [p.name for p in owner.pets]
    pet_filter = st.selectbox("Filter by pet", pet_filter_options, label_visibility="collapsed")

if scheduler.scheduled_tasks:
    # Build a pet-name lookup keyed by object id (Task is unhashable by default)
    task_to_pet = {
        id(task): p.name
        for p in owner.pets
        for task in p.tasks
    }

    # Use Scheduler methods for sorted + filtered data
    filter_pet = None if pet_filter == "All pets" else pet_filter
    sorted_tasks = scheduler.sort_by_time()
    if filter_pet:
        sorted_tasks = [t for t in sorted_tasks if task_to_pet.get(id(t)) == filter_pet]

    pending = [t for t in sorted_tasks if not t.completed]
    done    = [t for t in sorted_tasks if t.completed]

    # --- Pending tasks table ---
    if pending:
        st.markdown("#### Pending")
        rows = [
            {
                "Time":        t.time.strftime("%I:%M %p"),
                "Task":        t.title,
                "Pet":         task_to_pet.get(id(t), "?"),
                "Priority":    t.priority.name,
                "Frequency":   t.frequency.value,
                "Description": t.description,
            }
            for t in pending
        ]
        st.table(rows)
    else:
        st.success("All tasks are completed — great work!")

    # --- Completed tasks table ---
    if done:
        with st.expander(f"Completed tasks ({len(done)})"):
            rows = [
                {
                    "Time":      t.time.strftime("%I:%M %p"),
                    "Task":      t.title,
                    "Pet":       task_to_pet.get(id(t), "?"),
                    "Priority":  t.priority.name,
                    "Frequency": t.frequency.value,
                }
                for t in done
            ]
            st.table(rows)

    # --- Summary metrics ---
    st.divider()
    total   = len(scheduler.scheduled_tasks)
    n_done  = sum(1 for t in scheduler.scheduled_tasks if t.completed)
    n_pend  = total - n_done
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Tasks",     total)
    m2.metric("Pending",         n_pend)
    m3.metric("Completed",       n_done)

else:
    st.info("Add tasks and click 'Generate Schedule' to see results.")
