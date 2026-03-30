from datetime import datetime
from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task


owner = Owner("Raul")

patch = Pet(name="Patch", species="Dog")
dolly = Pet(name="Dolly", species="Cat")

owner.add_pet(patch)
owner.add_pet(dolly)

# --- Normal tasks ---
owner.create_task(patch, Task(
    title="Morning Walk",
    description="30 min walk around the park",
    time=datetime(2026, 3, 29, 7, 0),
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

# --- CONFLICT 1: two tasks for different pets at the same time (14:30) ---
owner.create_task(dolly, Task(
    title="Vet Checkup",
    description="Annual wellness exam",
    time=datetime(2026, 3, 29, 14, 30),
    priority=Priority.HIGH,
    frequency=Frequency.ONCE,
))

owner.create_task(patch, Task(
    title="Grooming Appointment",
    description="Bath and trim",
    time=datetime(2026, 3, 29, 14, 30),   # same time as Vet Checkup
    priority=Priority.MEDIUM,
    frequency=Frequency.ONCE,
))

# --- CONFLICT 2: two tasks for the same pet at the same time (18:00) ---
owner.create_task(patch, Task(
    title="Evening Feed",
    description="1 cup of dry food",
    time=datetime(2026, 3, 29, 18, 0),
    priority=Priority.HIGH,
    frequency=Frequency.DAILY,
))

owner.create_task(patch, Task(
    title="Medication",
    description="Heartworm pill with food",
    time=datetime(2026, 3, 29, 18, 0),    # same time as Evening Feed, same pet
    priority=Priority.HIGH,
    frequency=Frequency.DAILY,
))


scheduler = Scheduler(owner)
scheduler.generate()

# --- Print full schedule ---
print("=== Full Schedule (sorted by time) ===\n")
for task in scheduler.sort_by_time():
    pet_name = next(p.name for p in owner.pets if task in p.tasks)
    print(f"  {task.time.strftime('%Y-%m-%d %I:%M %p')}  [{task.priority.name:<6}]  "
          f"{task.title}  ({pet_name})")

# --- Run conflict detection ---
print("\n=== Conflict Check ===\n")
conflicts = scheduler.get_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")

# --- Resolve one conflict by rescheduling, then re-check ---
print("\n>> Rescheduling 'Grooming Appointment' to 15:30 to resolve conflict...")
patch.tasks[1].update_time(datetime(2026, 3, 29, 15, 30))
scheduler.generate()

print("\n=== Conflict Check After Reschedule ===\n")
conflicts = scheduler.get_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")
