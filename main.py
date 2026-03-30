from datetime import datetime
from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task


owner = Owner("Raul")

patch = Pet(name="Patch", species="Dog")
dolly = Pet(name="Dolly", species="Cat")

owner.add_pet(patch)
owner.add_pet(dolly)


owner.create_task(patch, Task(
    title="Morning Walk",
    description="30 min walk around the park",
    time=datetime(2026, 3, 29, 7, 0),
    priority=Priority.HIGH,
    frequency=Frequency.DAILY,
))

owner.create_task(patch, Task(
    title="Evening Feed",
    description="1 cup of dry food",
    time=datetime(2026, 3, 29, 18, 0),
    priority=Priority.HIGH,
    frequency=Frequency.DAILY,
))


owner.create_task(dolly, Task(
    title="Clean Litter Box",
    description="Scoop and replace litter",
    time=datetime(2026, 3, 29, 9, 0),
    priority=Priority.MEDIUM,
    frequency=Frequency.DAILY,
))

owner.create_task(dolly, Task(
    title="Vet Checkup",
    description="Annual wellness exam",
    time=datetime(2026, 3, 29, 14, 30),
    priority=Priority.HIGH,
    frequency=Frequency.ONCE,
))


scheduler = Scheduler(owner)
scheduler.generate()

print(f"=== Today's Schedule for {owner.name} ===\n")
for task in scheduler.scheduled_tasks:
    pet_name = next(
        (pet.name for pet in owner.pets if task in pet.tasks), "Unknown"
    )
    print(f"  {task.time.strftime('%I:%M %p')}  [{task.priority.name}]  {task.title}  ({pet_name})")
    print(f"           {task.description}")
    print()
