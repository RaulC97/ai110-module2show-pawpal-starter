import sys
import os
import unittest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task


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


def make_owner_with_pet(pet_name="Bella", species="Dog"):
    owner = Owner("Alex")
    pet = Pet(name=pet_name, species=species)
    owner.add_pet(pet)
    return owner, pet


class TestSchedulerSortingCorrectness(unittest.TestCase):
    """Verify tasks come back in chronological order after generate()."""

    def test_tasks_sorted_by_time_ascending(self):
        owner, pet = make_owner_with_pet()
        t1 = Task("Evening Walk",  "desc", datetime(2026, 3, 29, 18, 0), Priority.LOW)
        t2 = Task("Morning Feed",  "desc", datetime(2026, 3, 29,  7, 0), Priority.LOW)
        t3 = Task("Afternoon Med", "desc", datetime(2026, 3, 29, 13, 0), Priority.LOW)
        for t in (t1, t2, t3):
            pet.add_task(t)

        scheduler = Scheduler(owner)
        scheduler.generate()
        times = [t.time for t in scheduler.scheduled_tasks]

        self.assertEqual(times, sorted(times))

    def test_same_time_higher_priority_comes_first(self):
        owner, pet = make_owner_with_pet()
        slot = datetime(2026, 3, 29, 9, 0)
        low  = Task("Low task",  "desc", slot, Priority.LOW)
        high = Task("High task", "desc", slot, Priority.HIGH)
        pet.add_task(low)
        pet.add_task(high)

        scheduler = Scheduler(owner)
        scheduler.generate()
        result = scheduler.scheduled_tasks

        # HIGH priority should appear before LOW at the same timestamp
        self.assertEqual(result[0].priority, Priority.HIGH)
        self.assertEqual(result[1].priority, Priority.LOW)

    def test_sort_by_time_helper_matches_generate_order(self):
        owner, pet = make_owner_with_pet()
        t1 = Task("Task A", "desc", datetime(2026, 3, 29, 10, 0), Priority.MEDIUM)
        t2 = Task("Task B", "desc", datetime(2026, 3, 29,  8, 0), Priority.MEDIUM)
        pet.add_task(t1)
        pet.add_task(t2)

        scheduler = Scheduler(owner)
        scheduler.generate()

        self.assertEqual(scheduler.sort_by_time(), scheduler.scheduled_tasks)


class TestRecurrenceLogic(unittest.TestCase):
    """Completing a recurring task should schedule the next occurrence."""

    def test_completing_daily_task_adds_next_day_task(self):
        owner, pet = make_owner_with_pet()
        task = Task("Daily Feed", "desc", datetime(2026, 3, 29, 8, 0),
                    Priority.MEDIUM, Frequency.DAILY)
        pet.add_task(task)

        scheduler = Scheduler(owner)
        scheduler.generate()
        scheduler.mark_task_complete(task)

        pending_times = [t.time for t in pet.get_pending_tasks()]
        self.assertIn(datetime(2026, 3, 30, 8, 0), pending_times)

    def test_completing_weekly_task_adds_seven_day_offset(self):
        owner, pet = make_owner_with_pet()
        task = Task("Weekly Bath", "desc", datetime(2026, 3, 29, 10, 0),
                    Priority.LOW, Frequency.WEEKLY)
        pet.add_task(task)

        scheduler = Scheduler(owner)
        scheduler.generate()
        scheduler.mark_task_complete(task)

        pending_times = [t.time for t in pet.get_pending_tasks()]
        self.assertIn(datetime(2026, 4, 5, 10, 0), pending_times)

    def test_completing_once_task_creates_no_next_occurrence(self):
        owner, pet = make_owner_with_pet()
        task = Task("Vet Visit", "desc", datetime(2026, 3, 29, 9, 0),
                    Priority.HIGH, Frequency.ONCE)
        pet.add_task(task)

        scheduler = Scheduler(owner)
        scheduler.generate()
        scheduler.mark_task_complete(task)

        self.assertEqual(len(pet.get_pending_tasks()), 0)

    def test_new_occurrence_inherits_priority_and_frequency(self):
        owner, pet = make_owner_with_pet()
        task = Task("Daily Med", "desc", datetime(2026, 3, 29, 8, 0),
                    Priority.HIGH, Frequency.DAILY)
        pet.add_task(task)

        scheduler = Scheduler(owner)
        scheduler.generate()
        scheduler.mark_task_complete(task)

        next_task = pet.get_pending_tasks()[0]
        self.assertEqual(next_task.priority, Priority.HIGH)
        self.assertEqual(next_task.frequency, Frequency.DAILY)

    def test_completed_task_does_not_appear_in_pending(self):
        owner, pet = make_owner_with_pet()
        task = Task("Daily Feed", "desc", datetime(2026, 3, 29, 8, 0),
                    Priority.LOW, Frequency.DAILY)
        pet.add_task(task)

        scheduler = Scheduler(owner)
        scheduler.generate()
        scheduler.mark_task_complete(task)

        self.assertNotIn(task, scheduler.get_pending())


class TestConflictDetection(unittest.TestCase):
    """Scheduler.get_conflicts() should flag time slots with 2+ pending tasks."""

    def test_no_conflict_when_tasks_at_different_times(self):
        owner, pet = make_owner_with_pet()
        pet.add_task(Task("Feed",  "desc", datetime(2026, 3, 29,  8, 0), Priority.LOW))
        pet.add_task(Task("Walk",  "desc", datetime(2026, 3, 29, 10, 0), Priority.LOW))

        scheduler = Scheduler(owner)
        self.assertEqual(scheduler.get_conflicts(), [])

    def test_conflict_flagged_for_two_tasks_at_same_time(self):
        owner = Owner("Alex")
        pet1 = Pet("Bella", "Dog")
        pet2 = Pet("Mochi", "Cat")
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        slot = datetime(2026, 3, 29, 9, 0)
        pet1.add_task(Task("Walk Bella",    "desc", slot, Priority.HIGH))
        pet2.add_task(Task("Feed Mochi",    "desc", slot, Priority.MEDIUM))

        scheduler = Scheduler(owner)
        conflicts = scheduler.get_conflicts()

        self.assertEqual(len(conflicts), 1)
        self.assertIn("Walk Bella", conflicts[0])
        self.assertIn("Feed Mochi", conflicts[0])

    def test_completed_tasks_excluded_from_conflict_check(self):
        owner, pet = make_owner_with_pet()
        slot = datetime(2026, 3, 29, 9, 0)
        done_task    = Task("Done Task",    "desc", slot, Priority.LOW)
        pending_task = Task("Pending Task", "desc", slot, Priority.HIGH)
        done_task.mark_complete()
        pet.add_task(done_task)
        pet.add_task(pending_task)

        scheduler = Scheduler(owner)
        self.assertEqual(scheduler.get_conflicts(), [])

    def test_multiple_conflict_slots_all_reported(self):
        owner = Owner("Alex")
        pet1 = Pet("Bella", "Dog")
        pet2 = Pet("Mochi", "Cat")
        owner.add_pet(pet1)
        owner.add_pet(pet2)

        slot1 = datetime(2026, 3, 29,  9, 0)
        slot2 = datetime(2026, 3, 29, 14, 0)
        pet1.add_task(Task("Task A", "desc", slot1, Priority.HIGH))
        pet2.add_task(Task("Task B", "desc", slot1, Priority.LOW))
        pet1.add_task(Task("Task C", "desc", slot2, Priority.MEDIUM))
        pet2.add_task(Task("Task D", "desc", slot2, Priority.MEDIUM))

        scheduler = Scheduler(owner)
        conflicts = scheduler.get_conflicts()

        self.assertEqual(len(conflicts), 2)


if __name__ == "__main__":
    unittest.main()
