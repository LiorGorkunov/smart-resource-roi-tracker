"""Task collection for managing multiple tasks.

This module defines ``TaskCollection``: a simple container that stores
multiple ``Task`` objects so a project manager can work with and
compare several tasks at once.

``TaskCollection`` intentionally performs no ROI calculations and does
not modify the ``Task`` model (see ``task.Task``). Its single
responsibility is storing and returning ``Task`` objects.
"""

from task import Task


class TaskCollection:
    """A collection of ``Task`` objects.

    Tasks are stored in the order they are added. Adding a task never
    replaces or removes existing tasks.
    """

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the collection.

        Args:
            task: The ``Task`` object to add.

        Raises:
            TypeError: If ``task`` is not a ``Task`` instance.
        """
        if not isinstance(task, Task):
            raise TypeError(f"task must be a Task instance, got {task!r}.")
        self._tasks.append(task)

    def get_all_tasks(self) -> list[Task]:
        """Return all stored tasks, in the order they were added.

        Returns:
            A new list containing all stored tasks. Mutating the
            returned list does not affect the collection.
        """
        return list(self._tasks)

    def count(self) -> int:
        """Return the number of tasks currently stored in the collection."""
        return len(self._tasks)
