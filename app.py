"""
PawPal+ Streamlit UI — connected to pawpal_system.py backend.
Run with: streamlit run app.py
"""

import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling for busy owners.")

# ── Session state: persist Owner across reruns ────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

# ─────────────────────────────────────────────
# Step 1: Create Owner
# ─────────────────────────────────────────────
st.header("1. Owner Setup")
owner_name = st.text_input("Your name", value="Jordan")
if st.button("Create / Reset Owner"):
    st.session_state.owner = Owner(name=owner_name)
    st.success(f"Owner '{owner_name}' created!")

if st.session_state.owner is None:
    st.info("👆 Create an owner to get started.")
    st.stop()

owner: Owner = st.session_state.owner

# ─────────────────────────────────────────────
# Step 2: Add a Pet
# ─────────────────────────────────────────────
st.header("2. Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    # Avoid duplicate pet names
    existing_names = [p.name.lower() for p in owner.pets]
    if pet_name.lower() in existing_names:
        st.warning(f"A pet named '{pet_name}' already exists.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("**Current pets:**", [str(p) for p in owner.pets])

# ─────────────────────────────────────────────
# Step 3: Add a Task
# ─────────────────────────────────────────────
st.header("3. Schedule a Task")

if not owner.pets:
    st.info("Add at least one pet before scheduling tasks.")
else:
    pet_options = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_options)

    col1, col2 = st.columns(2)
    with col1:
        task_desc = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="07:00")
    with col2:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add Task"):
        selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        selected_pet.add_task(Task(
            description=task_desc,
            time=task_time,
            frequency=frequency,
            priority=priority,
        ))
        st.success(f"Task '{task_desc}' added to {selected_pet_name}!")

# ─────────────────────────────────────────────
# Step 4: Generate Schedule
# ─────────────────────────────────────────────
st.header("4. Today's Schedule")

if st.button("Generate Schedule"):
    if not owner.get_all_tasks():
        st.warning("No tasks found. Add some tasks first!")
    else:
        scheduler = Scheduler(owner)

        # Conflict warnings
        conflicts = scheduler.get_conflicts()
        if conflicts:
            for c in conflicts:
                st.warning(c)

        # Sorted schedule as a table
        sorted_tasks = scheduler.sort_by_time()
        table_data = [
            {
                "Time": t.time,
                "Task": t.description,
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Done": "✅" if t.completed else "⏳",
            }
            for t in sorted_tasks
        ]
        st.table(table_data)

        # Summary
        st.success(f"📋 {len(sorted_tasks)} task(s) scheduled for {owner.name}'s pets.")