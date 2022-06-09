"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


class Database:
    """A qme database holds common functions to represent tasks, and results.
    This is literally the base of the database, so it holds common shared
    functions to generate a task id or similar. The child classes (the
    specific database types) should have an init functions that ensures
    connection or creation of folders is possible.
    """

    database = "notimplemented"

    def clear(self):
        """clear (delete) all tasks."""
        raise NotImplementedError

    def search(self, query):
        """search is only available to non-filesystem databases"""
        raise NotImplementedError

    def list_tasks(self, name=None):
        """list tasks associated with an executor, or all tasks.

        Arguments:
        - executor (str) : the executor type. If not provided, list all
        """
        raise NotImplementedError

    def add_task(self, executor):
        """Create a filesystem task based on an executor type. The executor controls
        what data is exported and the uid, the task object just handles saving it.
        """
        raise NotImplementedError

    def update_task(self, executor, updates=None):
        """update a task with a json dictionary."""
        raise NotImplementedError

    def get_task(self, taskid=None):
        """Get a task based on a taskid. Exits on error if doesn't exist. If
        a task id is not provided, get the last run task.
        """
        raise NotImplementedError

    def delete_task(self, taskid):
        """delete a task based on a specific task id. All task ids must be
        in the format of <taskid>-<uid> without extra dashes so we can
        reliably split based on the first dash.
        """
        raise NotImplementedError

    def delete_executor(self, name):
        """delete all tasks for an executor, based on executor's name (str)."""
        raise NotImplementedError

    def iter_executors(self, fullpath=False):
        """list executors based on the subfolders in the base database folder."""
        raise NotImplementedError
