"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.exceptions import MissingImportError
import json


try:
    from sqlalchemy import Column, DateTime, String, Text, func
    from sqlalchemy.ext.declarative import declarative_base
except:
    raise MissingImportError("sqlalchemy", "is required for a non-filesystem database.")

# Shared declarative base
Base = declarative_base()


class Task(Base):
    """An executor task. The id is prefixed with the executor type, and must
    be unique.
    """

    __tablename__ = "task"
    taskid = Column(String(150), primary_key=True)
    command = Column(String(500))
    timestamp = Column(DateTime, default=func.now())
    executor_name = Column(String(50))
    data = Column(Text, nullable=True)

    def __init__(self, taskid=None, executor=None, command=None):
        self.taskid = taskid
        self.executor_name = executor
        self.command = command

    def summary(self):
        return self.executor.summary()

    def load(self):
        """loading a task means exporting as json"""
        data = {
            "executor": self.executor_name,
            "uid": self.taskid,
            "data": {},
            "command": self.command,
        }

        if self.data:
            data["data"] = json.loads(self.data)

        return data

    def export(self):
        """Export removes the outer wrapper, and just returns the data"""
        return self.load().get("data", {})

    def run_action(self, name, **kwargs):
        """Run an action, meaning that we prepare data to it, and then run
        the self.executor.run_action(name, data) function.
        """
        return self.executor.run_action(name, self.export(), **kwargs)

    def __repr__(self):
        return "<Task %r>" % self.taskid
