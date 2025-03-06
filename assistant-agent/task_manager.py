import json
import os

#Simple task management utility for storing tasks
task_file = "tasks.json"

# Load existing tasks if available
def load_tasks():
    if os.path.exists(task_file):
        with open(task_file, "r") as f:
            return json.load(f)
    return {}


def save_tasks(tasks):
    with open(task_file, "w") as f:
        json.dump(tasks, f, indent=4)


def create_task(task_id, task_description):
    """Create a new task with a unique task_id and description."""
    tasks = load_tasks()
    if task_id in tasks:
        return f"Task with ID {task_id} already exists."

    tasks[task_id] = task_description
    save_tasks(tasks)
    return f"Task '{task_description}' created successfully."


def remove_task(task_id):
    """Remove a task by its ID."""
    tasks = load_tasks()
    if task_id not in tasks:
        return f"Task with ID {task_id} not found."

    del tasks[task_id]
    save_tasks(tasks)
    return f"Task '{task_id}' removed successfully."


def list_tasks():
    """List all current tasks."""
    tasks = load_tasks()
    return tasks if tasks else "No tasks available."


if __name__ == "__main__":
    print("Task Manager initialized.")
    print(list_tasks())
