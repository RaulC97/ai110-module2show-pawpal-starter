from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    name: str


@dataclass
class Task:
    priority: str
    time: str

    def update_priority(self, priority: str):
        pass

    def update_time(self, time: str):
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []

    def add_pet(self, pet: Pet):
        pass

    def create_task(self, task: Task):
        pass


class Schedule:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled_tasks: List[Task] = []

    def generate(self):
        pass
