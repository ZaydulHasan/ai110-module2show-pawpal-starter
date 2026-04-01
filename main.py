"""
CLI demo script for PawPal+.
Run with: python main.py
"""

from pawpal_system import Task, Pet, Owner, Scheduler

# ── Create owner and pets ─────────────────────────────────────────────
owner = Owner(name="Jordan")

dog = Pet(name="Mochi", species="dog", age=3)
cat = Pet(name="Luna", species="cat", age=5)

owner.add_pet(dog)
owner.add_pet(cat)

# ── Add tasks to Mochi (dog) ──────────────────────────────────────────
dog.add_task(Task(description="Morning walk",      time="07:00", frequency="daily",  priority="high"))
dog.add_task(Task(description="Evening walk",      time="18:00", frequency="daily",  priority="high"))
dog.add_task(Task(description="Flea medication",   time="09:00", frequency="weekly", priority="medium"))

# ── Add tasks to Luna (cat) ───────────────────────────────────────────
cat.add_task(Task(description="Feed breakfast",    time="07:30", frequency="daily",  priority="high"))
cat.add_task(Task(description="Clean litter box",  time="09:00", frequency="daily",  priority="medium"))  # conflict with flea med!
cat.add_task(Task(description="Vet appointment",   time="14:00", frequency="once",   priority="high"))

# ── Create scheduler and print today's schedule ───────────────────────
scheduler = Scheduler(owner)

print(scheduler.todays_schedule())

# ── Demo: sorting ─────────────────────────────────────────────────────
print("\n--- Sorted by time ---")
for task in scheduler.sort_by_time():
    print(task)

# ── Demo: filtering incomplete tasks ─────────────────────────────────
print("\n--- Incomplete tasks ---")
for task in scheduler.filter_by_status(completed=False):
    print(task)

# ── Demo: complete a recurring task ──────────────────────────────────
print("\n--- Completing 'Morning walk' (daily recurring) ---")
morning_walk = dog.tasks[0]
scheduler.complete_task(morning_walk, dog)
print(f"Mochi now has {dog.task_count()} tasks (new walk added for tomorrow)")
print(f"Last task: {dog.tasks[-1]}")