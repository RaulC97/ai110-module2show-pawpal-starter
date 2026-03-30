from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Frequency(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Task:
    title: str
    description: str
    time: datetime
    priority: Priority
    frequency: Frequency = Frequency.ONCE
    completed: bool = False

    def update_priority(self, priority: Priority):
        """Set a new priority level for this task."""
        self.priority = priority

    def update_time(self, time: datetime):
        """Reschedule this task to a new datetime."""
        self.time = time

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return (f"[{status}] {self.title} | {self.priority.name} priority | "
                f"{self.frequency.value} | {self.time.strftime('%Y-%m-%d %H:%M')}")


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return all tasks that have been completed."""
        return [t for t in self.tasks if t.completed]

    def __str__(self):
        return f"{self.name} ({self.species}) — {len(self.tasks)} task(s)"


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def create_task(self, pet: Pet, task: Task):
        """Assign a task to one of the owner's pets, raising an error if the pet is unrecognized."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} does not belong to {self.name}")
        pet.add_task(task)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_pet(self, name: str) -> Optional[Pet]:
        """Look up a pet by name (case-insensitive), returning None if not found."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def __str__(self):
        return f"Owner: {self.name} | {len(self.pets)} pet(s)"


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled_tasks: List[Task] = []

    def generate(self):
        """Collect and sort all owner tasks by time, then by descending priority."""
        all_tasks = self.owner.get_all_tasks()
        self.scheduled_tasks = sorted(
            all_tasks,
            key=lambda t: (t.time, -t.priority.value)
        )

    def get_pending(self) -> List[Task]:
        """Return all scheduled tasks that are not yet completed."""
        return [t for t in self.scheduled_tasks if not t.completed]

    def get_by_priority(self, priority: Priority) -> List[Task]:
        """Return all scheduled tasks matching the given priority level."""
        return [t for t in self.scheduled_tasks if t.priority == priority]

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks assigned to a pet by name, or an empty list if not found."""
        pet = self.owner.get_pet(pet_name)
        if not pet:
            return []
        return pet.tasks

    def summary(self):
        """Print a full schedule report with total, completed, and pending task counts."""
        self.generate()
        total = len(self.scheduled_tasks)
        done = sum(1 for t in self.scheduled_tasks if t.completed)
        pending = total - done
        print(f"\n=== Schedule for {self.owner.name} ===")
        print(f"Total: {total} | Completed: {done} | Pending: {pending}\n")
        for task in self.scheduled_tasks:
            print(f"  {task}")
        print()
