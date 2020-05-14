"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.defaults import QME_DATABASE
from qme.main.config import Config
from qme.main.database import init_db
from qme.main.executor import get_executor, get_named_executor
from qme.logger import bot

import os
import sys


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
        # update database settings
        self.config.update(
            section="DEFAULT",
            key="database",
            value=database or self.config.get("DEFAULT", "database"),
        )
        self.database = self.config.get("DEFAULT", "database")
        bot.info("DATABASE: %s" % self.database)

        # Supported database options
        valid = ("sqlite", "postgres", "mysql", "filesystem")
        if not self.database.startswith(valid):
            bot.warning(
                "%s is not yet a supported type, saving to filesystem." % self.database
            )
            self.database = "filesystem"

        # Create database client with functions for database type
        self.db = init_db(self.database, config_dir=self.config_dir)

    def list(self, executor=None):
        """A wrapper to the database list_tasks function. Optionally take
           a whole executor name (e.g., shell) or just a specific task. No
           executor indicates that we list everything.
        """
        self.db.list_tasks(executor)

    def get(self, taskid):
        """A wrapper to get a task id from the database.
        """
        executor = taskid.split("-", 1)[0]
        executor = get_named_executor(executor, taskid)
        return self.db.get_task(executor)

    def run(self, command):
        """Given a command, get the executor for it (also creating an entry
           in the task database) and run the command.
        """
        executor = get_executor()

        # add executor unique id and command to the database, returns a task object
        task = self.db.add_task(executor)

        # Execute and store result (this will need to be generalized)
        executor.execute(command)
        self.db.update_task(executor)
        bot.info(f"{task.summary()}")
