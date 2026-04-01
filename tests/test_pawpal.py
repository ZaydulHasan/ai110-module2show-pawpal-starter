"""
Automated tests for PawPal+ system.
Run with: python -m pytest
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Helpers ───────────────────────────────────────────────────────────

def make_scheduler():
    """Create a fresh owner with two pets and several tasks for testing."""
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna", species="cat", age=5)

    dog.add_task(Task(description="Morning walk",   time="07:00", frequency="daily",  priority="high"))
    dog.add_task(Task(description="Evening walk",   time="18:00", frequency="daily",  priority="high"))
    cat.add_task(Task(description="Feed breakfast", time="07:30", frequency="daily",  priority="high"))
    cat.add_task(Task(description="Vet visit",      time="14:00", frequency="once",   priority="high"))

    owner.add_pet(dog)
    owner.add_pet(cat)
    return Scheduler(owner), dog, cat


# ── Test: Task completion changes status ──────────────────────────────

def test_mark_complete_changes_status():
    task = Task(description="Walk", time="08:00", frequency="once", priority="low")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# ── Test: Adding a task increases pet task count ──────────────────────

def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="dog", age=2)
    assert pet.task_count() == 0
    pet.add_task(Task(description="Walk", time="08:00", frequency="once", priority="low"))
    assert pet.task_count() == 1
    pet.add_task(Task(description="Feed", time="09:00", frequency="daily", priority="high"))
    assert pet.task_count() == 2


# ── Test: Sorting returns tasks in chronological order ────────────────

def test_sort_by_time():
    scheduler, _, _ = make_scheduler()
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times), "Tasks are not in chronological order"


# ── Test: Daily recurring task creates next-day task ─────────────────

def test_daily_recurrence():
    pet = Pet(name="Mochi", species="dog", age=3)
    today = date.today()
    task = Task(description="Walk", time="07:00", frequency="daily",
                priority="high", due_date=today)
    pet.add_task(task)

    owner = Owner(name="Jordan")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    scheduler.complete_task(task, pet)

    assert task.completed is True
    assert pet.task_count() == 2  # original + new recurring
    new_task = pet.tasks[-1]
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.completed is False


# ── Test: Conflict detection flags duplicate times ────────────────────

def test_conflict_detection():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", age=3)

    pet.add_task(Task(description="Walk",     time="09:00", frequency="once", priority="high"))
    pet.add_task(Task(description="Medicine", time="09:00", frequency="once", priority="medium"))

    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.get_conflicts()
    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]


# ── Test: No conflict when times are different ────────────────────────

def test_no_false_conflicts():
    scheduler, _, _ = make_scheduler()
    conflicts = scheduler.get_conflicts()
    assert len(conflicts) == 0