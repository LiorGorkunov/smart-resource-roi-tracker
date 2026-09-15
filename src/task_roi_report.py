"""ROI reporting for a collection of tasks.

This module implements SCRUM-7: calculating the ROI of every ``Task``
in a ``TaskCollection``. It reuses ``roi_calculator.calculate_roi``
(SCRUM-4) rather than duplicating the ROI formula, and does not modify
``Task`` (SCRUM-5) or ``TaskCollection`` (SCRUM-6).

No sorting or prioritization is performed here; results are returned
in the same order as ``TaskCollection.get_all_tasks()``.
"""

from roi_calculator import calculate_roi
from task import Task
from task_collection import TaskCollection


def calculate_roi_for_task(task: Task) -> dict:
    """Calculate the ROI result for a single task.

    Args:
        task: The ``Task`` to evaluate.

    Returns:
        A dictionary with the following keys:
            - "task": the original ``Task`` instance.
            - "roi": the ``dict`` returned by ``calculate_roi`` for
              this task's hours, hourly rate, and expected benefit.
    """
    roi = calculate_roi(task.hours, task.hourly_rate, task.expected_benefit)
    return {"task": task, "roi": roi}


def calculate_roi_for_collection(collection: TaskCollection) -> list[dict]:
    """Calculate the ROI result for every task in a collection.

    Args:
        collection: The ``TaskCollection`` whose tasks should be
            evaluated.

    Returns:
        A list of dictionaries, one per task, in the same order as
        ``collection.get_all_tasks()``. Each dictionary has the shape
        described in ``calculate_roi_for_task``. Returns an empty list
        if the collection is empty.
    """
    return [calculate_roi_for_task(task) for task in collection.get_all_tasks()]
