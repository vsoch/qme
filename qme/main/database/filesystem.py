"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.exceptions import (
    DirectoryNotFoundError,
    MultipleTasksExistError,
    TaskNotFoundError,
)
from qme.utils.file import (
    write_json,
    mkdir_p,
    read_json,
    recursive_find,
    get_latest_modified,
)
from qme.main.database.base import Database
from qme.main.executor import get_named_executor
from glob import glob
import logging
import shutil
import os
import re

bot = logging.getLogger("qme.main.database.filesystem")


class FileSystemDatabase(Database):
    """A FileSystemDatabase writes raw json to files at $HOME/.qme/database
    This is the default flat database for qme, and on init we ensure
    that the database folder is created in QME_HOME.
    """

    database = "filesystem"

    def __init__(self, config_dir, config=None, **kwargs):
        """init for the filesystem ensures that the base folder (named
        according to the studyid) exists.
        """
        self.config = config
        self.create_database(config_dir)

    def create_database(self, config_dir):
        """Create the database. The parent folder must exist."""
        self.data_base = os.path.abspath(os.path.join(config_dir, "database"))
        if not os.path.exists(config_dir):
            raise DirectoryNotFoundError(
                config_dir, "must exist to create database there"
            )
        if not os.path.exists(self.data_base):
            mkdir_p(self.data_base)

    # Global

    def clear(self):
        """clear (delete) all tasks."""
        for executor_dir in self.iter_executors(fullpath=True):
            if os.path.exists(executor_dir):
                bot.info(f"Removing {executor_dir}")
                shutil.rmtree(executor_dir)
        return True

    # Add or Update requires executor

    def add_task(self, executor):
        """Create a filesystem task based on an executor type. The executor controls
        what data is exported and the uid, the task object just handles saving it.
        """
        return FileSystemTask(executor, data_base=self.data_base)

    def update_task(self, executor, updates=None):
        """update a task with a json dictionary."""
        task = FileSystemTask(executor, exists=True, data_base=self.data_base)
        task.update({"data": executor.export(), "command": executor.command})

    # Get, delete, etc. only require taskid

    def get_task(self, taskid=None):
        """Get a task based on a taskid. Exits on error if doesn't exist. If
        a task id is not provided, get the last run task.
        """
        if not taskid:
            taskid = os.path.basename(
                get_latest_modified(self.data_base, pattern="*.json")
            ).replace(".json", "")
        executor = taskid.split("-", 1)[0]
        executor = get_named_executor(executor, taskid, config=self.config)
        return FileSystemTask(executor, exists=True, data_base=self.data_base)

    def delete_task(self, taskid):
        """delete a task based on a specific task id. All task ids must be
        in the format of <taskid>-<uid> without extra dashes so we can
        reliably split based on the first dash.
        """
        task = self.get_task(taskid)
        if not task:
            bot.error(f"{taskid} does not exist in the database.")
            return False
        os.remove(task.filename)
        bot.info(f"{taskid} has been removed.")
        return True

    def delete_executor(self, name):
        """delete all tasks for an executor, based on executor's name (str)."""
        executor_dir = os.path.join(self.data_base, name)
        if not os.path.exists(executor_dir):
            bot.error(f"Executor {executor_dir} directory does not exist.")
            return False
        shutil.rmtree(executor_dir)
        return True

    def iter_executors(self, fullpath=False):
        """list executors based on the subfolders in the base database folder."""
        for contender in os.listdir(self.data_base):
            contender = os.path.join(self.data_base, contender)
            if os.path.isdir(contender):
                if not fullpath:
                    yield os.path.basename(contender)
                else:
                    yield contender

    def list_tasks(self, name=None):
        """list tasks, either under a particular executor name (if provided)
        or just the executors. This returns tasks in rows to be printed
        (or otherwise parsed).
        """
        listpath = self.data_base
        if name:
            listpath = os.path.join(listpath, name)
        rows = []
        for filename in recursive_find(listpath, pattern="*.json"):
            rows.append([os.path.basename(filename).replace(".json", "")])
        return rows


class FileSystemTask:
    """A Filesystem Task can take a task id, determine if the task exists,
    and then interact with the data. If the task is instantiated without
    a taskid it is assumed to not exist yet, otherwise it must already
    exist.
    """

    def __init__(self, executor, data_base, exists=False):
        """A FileSystem task tasks some task id and command for an executor.
        We provide a simple interface to retrieve the data file, and
        do an initial creation if it doesn't exist.

        Arguments:
          taskid (str) : the executor-uuid for the task
          command (list) : the command to be executed
          data_base (str) : the path where the database exists.
          exists (bool) : if True, must already exists (default is False)
        """
        self.taskid = executor.taskid
        self.executor = executor
        self.data_base = data_base
        self.data = {}
        self.create(exists)

    @property
    def filename(self):
        return "%s.json" % os.path.join(self.executor_dir, self.executor.taskid)

    @property
    def executor_dir(self):
        return os.path.join(self.data_base, self.executor.name)

    def update(self, updates=None):
        """Update a data file. This means reading, updating, and writing."""
        updates = updates or {}
        if updates:
            self.data.update(updates)
            self.save()

    def create(self, should_exist=False):
        """create the filename if it doesn't exist, otherwise if it should (and
        does not) exit on error.
        """
        if should_exist:
            if not os.path.exists(self.filename):

                # Might be provided prefix
                contenders = glob(
                    "%s*" % os.path.join(self.executor_dir, self.executor.taskid)
                )
                if len(contenders) == 1:
                    self.executor.taskid = re.sub(
                        "(%s/|[.]json)"
                        % os.path.join(self.data_base, self.executor.name),
                        "",
                        contenders[0],
                    )

                elif len(contenders) > 1:
                    raise MultipleTasksExistError(self.executor.taskid)
                else:
                    raise TaskNotFoundError(self.executor.taskid)
            self.data = self.load()

        if not os.path.exists(self.executor_dir):
            os.mkdir(self.executor_dir)

        # If it's the first time saving, create basic file
        if not should_exist:
            self.data = {
                "executor": self.executor.name,
                "uid": self.executor.taskid,
                "command": self.executor.command,
                "data": self.executor.export(),
            }
            self.save()

    def export(self):
        """wrapper to expose the executor.export function"""
        return self.executor.export()

    def save(self):
        """Save a json object to the task."""
        write_json(self.data, self.filename)

    def summary(self):
        return self.executor.summary()

    def load(self):
        """Given a task, load data from filename."""
        if os.path.exists(self.filename):
            return read_json(self.filename)

    def run_action(self, name, **kwargs):
        """Run an action, meaning running the executor's run_action but
        providing data from the database.
        """
        return self.executor.run_action(name, self.data, **kwargs)
