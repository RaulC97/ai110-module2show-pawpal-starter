import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pawpal_system import Frequency, Owner, Pet, Priority, Task


def make_task(title="Test Task", priority=Priority.LOW, time=None):
    return Task(
        title=title,
        description="A test task",
        time=time or datetime(2026, 3, 29, 9, 0),
        priority=priority,
    )


class TestTaskCompletion(unittest.TestCase):

    def test_task_starts_incomplete(self):
        task = make_task()
        self.assertFalse(task.completed)

    def test_mark_complete_changes_status(self):
        task = make_task()
        task.mark_complete()
        self.assertTrue(task.completed)

    def test_mark_complete_is_idempotent(self):
        task = make_task()
        task.mark_complete()
        task.mark_complete()
        self.assertTrue(task.completed)


class TestPetTaskAddition(unittest.TestCase):

    def test_new_pet_has_no_tasks(self):
        pet = Pet(name="Bella", species="Dog")
        self.assertEqual(len(pet.tasks), 0)

    def test_add_task_increases_count(self):
        pet = Pet(name="Bella", species="Dog")
        pet.add_task(make_task("Feed Bella"))
        self.assertEqual(len(pet.tasks), 1)

    def test_add_multiple_tasks_increases_count(self):
        pet = Pet(name="Bella", species="Dog")
        pet.add_task(make_task("Feed Bella"))
        pet.add_task(make_task("Walk Bella"))
        pet.add_task(make_task("Vet Visit"))
        self.assertEqual(len(pet.tasks), 3)

    def test_added_task_is_in_pet_tasks(self):
        pet = Pet(name="Mochi", species="Cat")
        task = make_task("Clean Litter")
        pet.add_task(task)
        self.assertIn(task, pet.tasks)


if __name__ == "__main__":
    unittest.main()
