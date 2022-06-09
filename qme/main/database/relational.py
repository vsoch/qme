"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.exceptions import (
    MissingDatabaseString,
    NoTasksError,
    MultipleTasksExistError,
    TaskNotFoundError,
)
from qme.main.database.base import Database
from qme.main.executor import get_named_executor

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import or_

import logging
import json

bot = logging.getLogger("qme.main.database.relational")


class RelationalDatabase(Database):
    """A RelationalDatabase is a more robust relational datbase (to sqlite).
    Since the global database property can be any of postgresql, mysql+pysq;,
    it is defined on init. The sqlite database also uses this class, but defines
    a custom init function to handle the $HOME/.qme/qme.db file.
    """

    def __init__(self, config_dir, config=None, **kwargs):
        """init for the filesystem ensures that the base folder (named
        according to the studyid) exists.
        """
        self.database = kwargs.get("database")
        self.config = config
        database_string = kwargs.get("database_string")
        if not database_string:
            raise MissingDatabaseString

        # The database url includes the type and string
        self.db = "%s://%s" % (self.database, database_string)
        self.create_database()

    def create_database(self):
        """create the databsae based on the string, whether it's relational or
        sqlite. self.db must be defined.
        """
        from qme.main.database.models import Base

        self.engine = create_engine(self.db)
        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        Base.query = self.session.query_property()
        Base.metadata.create_all(bind=self.engine)
        self.Base = Base

    # Global

    def clear(self):
        """clear (delete) all tasks. This could be improved to cascade instead."""
        from qme.main.database.models import Task

        Task.query.delete()
        self.session.commit()
        return True

    # Add or Update requires executor

    def add_task(self, executor):
        """Create a new task based on an executor type. The executor controls
        what data is exported and the uid, the task object just handles saving it.
        """
        from qme.main.database.models import Task

        task = Task(taskid=executor.taskid, executor=executor.name)
        self.session.add(task)
        self.session.commit()
        task.executor = executor
        return task

    def update_task(self, executor, updates=None):
        """update a task with a json dictionary."""
        from qme.main.database.models import Task

        task = Task.query.filter(Task.taskid == executor.taskid).first()
        updates = updates or {}
        updates.update(executor.export())

        # If we find a matching task
        if task:

            # If a command is defined
            if executor.command:
                task.command = executor.command

            # Load the previous data to update
            data = {}
            if task.data:
                data = json.loads(task.data)
            data.update(updates)

            task.data = json.dumps(data)
            self.session.add(task)
            self.session.commit()
            return task

    # Get, delete, etc. only require taskid

    def get_task(self, taskid=None):
        """Get a task based on a taskid. Exits on error if doesn't exist. If
        a task id is not provided, get the last run task.
        """
        from qme.main.database.models import Task

        # Retrieve either the last task, or the one with a specific taskid
        if not taskid:
            task = self.session.query(Task).order_by(desc("timestamp")).first()
            if not task:
                raise NoTasksError
        else:
            task = Task.query.filter(Task.taskid == taskid).first()

            # If an exact match isn't there, look for partial match
            if not task:
                query = "%" + taskid + "%"
                query = self.session.query(Task).filter(Task.taskid.ilike(query))
                results = self.session.execute(query).fetchall()
                if len(results) == 1:
                    return self.get_task(results[0][0])
                elif len(results) > 1:
                    raise MultipleTasksExistError(taskid)
                else:
                    raise TaskNotFoundError(taskid)

        # Add the executor to the task
        executor = task.taskid.split("-", 1)[0]
        task.executor = get_named_executor(executor, task.taskid, config=self.config)
        return task

    def delete_task(self, taskid):
        """delete a task based on a specific task id. All task ids must be
        in the format of <taskid>-<uid> without extra dashes so we can
        reliably split based on the first dash.
        """
        from qme.main.database.models import Task

        task = self.get_task(taskid)
        if not task:
            bot.error(f"{taskid} does not exist in the database.")
            return False
        Task.query.filter(Task.taskid == task.taskid).delete()
        self.session.commit()
        bot.info(f"{taskid} has been removed.")
        return True

    def delete_executor(self, name):
        """delete all tasks for an executor, based on executor's name (str)."""
        from qme.main.database.models import Task

        deleted_items = False
        for task in Task.query.filter(Task.executor_name == name):
            deleted_items = True
            self.session.delete(task)
        self.session.commit()
        return deleted_items

    def iter_executors(self, fullpath=False):
        """list executors based on the subfolders in the base database folder."""
        from qme.main.database.models import Task

        for executor in self.session.query(Task.executor_name).distinct():
            yield executor[0]

    def list_tasks(self, name=None):
        """list tasks, either under a particular executor name (if provided)
        or just the executors. This returns tasks in rows to be printed
        (or otherwise parsed).
        """
        from qme.main.database.models import Task

        if name:
            tasks = Task.query.filter(Task.executor_name == name)
        else:
            tasks = Task.query.all()

        rows = []
        for task in tasks:
            rows.append([task.taskid, task.command or ""])
        return rows

    def search(self, query):
        """Search across the database for a particular query."""
        from qme.main.database.models import Task

        # Ensure that query can be part of a larger string
        query = "%" + query + "%"

        query = self.session.query(Task).filter(
            or_(Task.command.ilike(query), Task.data.ilike(query))
        )
        # previously list of tuples, (taskid, command, datetime, executor]
        # Now list of tasks
        results = self.session.execute(query).fetchall()
        return [r[0] for r in results]
