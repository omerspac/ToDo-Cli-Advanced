import click
import json
import os

TODO_FILE = "todo.json"

def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []
        
def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent = 4)

@click.group()
def cli():
    """Simple ToDo CLI Manager"""
    pass

@click.command()
@click.argument("task")
def add(task):
    """Add a new task"""
    tasks = load_tasks()
    tasks.append({"title": task, "completed": False})
    save_tasks(tasks)
    click.echo(f"Task '{task}' added successfully.")

@click.command()
@click.argument("task_number", type = int)
def remove(task_number):
    """Remove a task"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):    
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Task removed: {removed_task['title']} successfully.")
    else:
        click.echo(f"Invalid task number: {task_number} | Please try again.")

@click.command()
def list():
    """Lists all tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found.")
        return
    for index, title in enumerate(tasks, 1):
        status = "✓" if title["completed"] else "X"
        click.echo(f"{index}. [{status}] {title['title']}")      

@click.command()
@click.argument("task_number", type = int)
def task_number():
    """Mark a task as completed"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed.")
    else:
        click.echo(f"Invalid task number: {task_number} | Please try again.")

@click.command()
def clear():
    """Clear all tasks"""
    tasks = load_tasks()
    tasks.clear()
    save_tasks(tasks)
    click.echo("All tasks cleared.")
        



# ALL COMMANDS FOR PROGRAM
cli.add_command(add)
cli.add_command(remove)
cli.add_command(list)
cli.add_command(task_number)
cli.add_command(clear)

if __name__ == "__main__":
    cli()