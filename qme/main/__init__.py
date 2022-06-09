"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.defaults import QME_DATABASE
from qme.exceptions import NotSupportedError, UnrecognizedTargetError
from qme.main.config import Config
from qme.main.database import init_db
from qme.main.executor import get_executor
from qme.utils.regex import uuid_regex
from qme.utils.prompt import confirm

import logging
import os
import re

bot = logging.getLogger("qme.main")


class Queue:
    """A Queue Me (qme) Queue is the core operator for the qme library. Here
    we initialize a queue, meaning:
    1. taking and setting up a user specified database or the default
    2. setting up a configuration file in $HOME (or at QME_HOME)
    3. then can be used to show a status, parse a job, etc.
    """

    def __init__(self, config_dir=None, database=None):
        """create a queue. We take a config directory (defaults to $HOME/.qme)
        and a database configuration string (defaults to filesystem to be
        created at $HOME/.qme/database
        """
        self.config = Config(config_dir)
        self.config_dir = os.path.dirname(self.config.configfile)
        self.initdb(database)

    def initdb(self, database):
        """setup the qme home (where the config directory is stored) and the
        database specification. If a database string is required (and not
        provided) alert the user and exit on error).

        Arguments:
         - config_dir (str) : the configuration directory (home for qme)
         - database (str) : a string to specify the database setup
        """
        self.database = (
            database
            or QME_DATABASE
            or self.config.get("DEFAULT", "database")
            or "filesystem"
        )
        database_string = self.config.get("DEFAULT", "databaseconnect")
        bot.info("Database: %s" % self.database)

        # Supported database options
        valid = ("sqlite", "postgresql", "mysql+pymysql", "filesystem")
        if not self.database.startswith(valid):
            bot.warning(
                "%s is not yet a supported type, saving to filesystem." % self.database
            )
            self.database = "filesystem"

        # Create database client with functions for database type
        self.db = init_db(
            self.database,
            config_dir=self.config_dir,
            database_string=database_string,
            config=self.config,
        )

    def list(self, executor=None):
        """A wrapper to the database list_tasks function. Optionally take
        a whole executor name (e.g., shell) or just a specific task. No
        executor indicates that we list everything.
        """
        return self.db.list_tasks(executor)

    def get(self, taskid=None):
        """A wrapper to get a task id from the database. If an id is not provided,
        will return the last run task based on timestamp of file or database.
        """
        return self.db.get_task(taskid)

    def clear(self, target=None, noprompt=False):
        """clear takes a target, and that can be a taskid, executor, or none
        We ask the user for confirmation.
        """
        # Case 1: no target indicates clearing all
        if not target:
            if noprompt or confirm("This will delete all tasks, are you sure?"):
                return self.db.clear()

        # Case 2, it's a specific taskid
        elif re.search(uuid_regex, target):
            if noprompt or confirm(f"This will delete task {target}, are you sure?"):
                return self.db.delete_task(target)

        # Case 2: it's an executor
        elif target in list(self.db.iter_executors()):
            if noprompt or confirm(
                f"This will delete all executor {target} tasks, are you sure?"
            ):
                return self.db.delete_executor(target)
        else:
            raise UnrecognizedTargetError(target, "to clear")

    def run(self, command, message=None):
        """Given a command, get the executor for it (also creating an entry
        in the task database) and run the command.
        """
        executor = get_executor(command, config=self.config)

        # add executor unique id and command to the database, returns a task object
        task = self.db.add_task(executor)

        # Execute and store result (this will need to be generalized)
        task.executor.execute(message=message)
        self.db.update_task(task.executor)
        bot.info(f"{task.summary()}")
        return task

    def rerun(self, taskid=None, message=None):
        """Given a command, get the executor for it (also creating an entry
        in the task database) and run the command. If the task is found and
        rerun, it is returned. Otherwise None is returned.
        """
        task = self.db.get_task(taskid)
        params = task.load()
        command = params.get("command")
        pwd = params.get("pwd")
        if pwd:
            os.chdir(pwd)
        if command:
            task.executor.execute(command, message=message)
            self.db.update_task(task.executor)
            bot.info(f"{task.summary()}")
            return task
        else:
            bot.warning(f"{task.executor.taskid} does not have an associated command.")

    def search(self, query):
        """Search across commands and general metadata for a string of interest.
        We use regular expressions (re.search) so they are supported.
        Search is only available for non-filesystem databases.
        """
        if self.database == "filesystem":
            raise NotSupportedError(
                "Search is only supported for relational databases."
            )
        return self.db.search(query)
