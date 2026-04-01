"""
PawPal+ backend logic.
Four classes: Task, Pet, Owner, Scheduler.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


# ─────────────────────────────────────────────
# Task
# ─────────────────────────────────────────────

@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str               # "HH:MM" format
    frequency: str          # "once", "daily", "weekly"
    priority: str           # "low", "medium", "high"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """
        Mark this task complete.
        If it recurs, return a new Task scheduled for the next occurrence.
        """
        self.completed = True
        if self.frequency == "daily":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                priority=self.priority,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly":
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                priority=self.priority,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None   # "once" tasks don't recur

    def __str__(self) -> str:
        status = "✅" if self.completed else "⏳"
        return f"{status} [{self.time}] {self.description} ({self.priority}, {self.frequency})"


# ─────────────────────────────────────────────
# Pet
# ─────────────────────────────────────────────

@dataclass
class Pet:
    """Stores pet details and owns a list of tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's list."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return the number of tasks for this pet."""
        return len(self.tasks)

    def __str__(self) -> str:
        return f"{self.name} ({self.species}, age {self.age}) — {self.task_count()} task(s)"


# ─────────────────────────────────────────────
# Owner
# ─────────────────────────────────────────────

@dataclass
class Owner:
    """Manages multiple pets and exposes all their tasks."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def __str__(self) -> str:
        return f"Owner: {self.name} | Pets: {[p.name for p in self.pets]}"


# ─────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────

class Scheduler:
    """Retrieves, organises, and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Initialise the scheduler with an owner."""
        self.owner = owner

    # ── Sorting ──────────────────────────────

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted chronologically by HH:MM time string."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    # ── Filtering ────────────────────────────

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks matching the given completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to a specific pet (case-insensitive)."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.tasks
        return []

    # ── Conflict detection ───────────────────

    def get_conflicts(self) -> List[str]:
        """
        Return a list of warning strings for tasks scheduled at the same time.
        Checks all tasks across all pets.
        """
        tasks = self.owner.get_all_tasks()
        seen: dict = {}
        warnings: List[str] = []

        for task in tasks:
            if task.time in seen:
                warnings.append(
                    f"⚠️  Conflict at {task.time}: "
                    f'"{seen[task.time]}" and "{task.description}"'
                )
            else:
                seen[task.time] = task.description

        return warnings

    # ── Recurring task completion ─────────────

    def complete_task(self, task: Task, pet: Pet) -> None:
        """
        Mark a task complete and, if it recurs, add the next occurrence
        to the same pet's task list.
        """
        next_task = task.mark_complete()
        if next_task:
            pet.add_task(next_task)

    # ── Schedule display ─────────────────────

    def todays_schedule(self) -> str:
        """Return a formatted string of today's schedule sorted by time."""
        tasks = self.sort_by_time()
        if not tasks:
            return "No tasks scheduled."

        lines = ["📅 Today's Schedule", "─" * 36]
        for task in tasks:
            lines.append(str(task))

        conflicts = self.get_conflicts()
        if conflicts:
            lines.append("\n" + "\n".join(conflicts))

        return "\n".join(lines)