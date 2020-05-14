"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys

# Common shared functions
# generate_taskid
# list_tasks
# generate_task
# save_task


class Database:
    """A qme database holds common functions to represent tasks, and results.
       This is literally the base of the database, so it holds common shared
       functions to generate a task id or similar. The child classes (the
       specific database types) should have an init functions that ensures
       connection or creation of folders is possible.
    """

    def generate_taskid(self, token=None):
        """assumes a flat (file system) database, organized by experiment id, and
           subject id, with data (json) organized by subject identifier
        """
        print("generate_taskid")

        # Headless doesn't use any folder_id, just generated token folder
        return "%s/%s" % (self.study_id, token)

    def list_tasks(self, executor=None):
        """list tasks associated with an executor, or all tasks.

           Arguments:
           - executor (str) : the executor type. If not provided, list all
        """
        raise NotImplementedError

    def generate_task(self, taskid=None):
        """generate a new task.

           Arguments:
            - taskid (str) : the identifier for the task
        """
        raise NotImplementedError

    def save_task(self, taskid, content):
        """save task will take the current taskid and save it to the database.

           Arguments:
            - taskid (str) : the identifier for the task
            - content (dict) : dictionary of content expected for the task
        """
        raise NotImplementedError
