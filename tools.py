from datetime import datetime
from memory import StudyMemory


# Create one memory instance for the current conversation
memory = StudyMemory()


def add_task(name, due):
    """Add a study task to memory."""

    try:
        datetime.strptime(due, "%Y-%m-%d").date()
    except ValueError:
        return {
            "success": False,
            "message": "Invalid date format. Use YYYY-MM-DD."
        }

    task = memory.add_task(name, due)

    return {
        "success": True,
        "message": f"Task '{name}' added successfully.",
        "task": task
    }


def build_schedule():
    """Build a schedule using tasks stored in memory."""

    tasks = memory.get_tasks()

    if not tasks:
        return {
            "success": False,
            "message": "No tasks available."
        }

    sorted_tasks = sorted(
        tasks,
        key=lambda task: datetime.strptime(
            task["due"], "%Y-%m-%d"
        ).date()
    )

    schedule = []

    for task in sorted_tasks:
        schedule.append({
            "task": task["name"],
            "deadline": task["due"]
        })

    return {
        "success": True,
        "schedule": schedule
    }


def get_tasks():
    """Return all tasks currently stored in memory."""

    return memory.get_tasks()