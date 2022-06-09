"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


class MissingEnvironmentVariable(RuntimeError):
    """Thrown if a required environment variable is not provided."""

    def __init__(self, varname, *args, **kwargs):
        super(MissingEnvironmentVariable, self).__init__(*args, **kwargs)
        self.varname = varname

    def __str__(self):
        return "Missing environment variable '{}' is required".format(self.varname)


class InvalidDatabaseFilename(ValueError):
    pass


class DirectoryNotFoundError(FileNotFoundError):
    """Thrown if a directory is not found"""

    def __init__(self, dirname, reason, *args, **kwargs):
        super(DirectoryNotFoundError, self).__init__(*args, **kwargs)
        self.dirname = dirname
        self.reason = reason

    def __str__(self):
        return "{} {}.".format(self.dirname, self.reason)


## Tasks


class TaskError(RuntimeError):
    """Abstract base class for any kind of TaskError."""

    def __init__(self, taskid=None, reason=None, *args, **kwargs):
        super(TaskError, self).__init__(*args, **kwargs)
        self.taskid = taskid or ""
        self.reason = reason or "There was a problem with task"

    def __str__(self):
        return "{} {}".format(self.reason, self.taskid)


class MultipleTasksExistError(TaskError):
    """Thrown if multiple tasks exist."""

    def __init__(self, taskid, *args, **kwargs):
        reason = "More than one task found for"
        super(MultipleTasksExistError, self).__init__(
            taskid=taskid, reason=reason, *args, **kwargs
        )


class TaskNotFoundError(TaskError):
    """Thrown if task does not exist."""

    def __init__(self, taskid, *args, **kwargs):
        reason = "Cannot find task"
        super(TaskNotFoundError, self).__init__(
            taskid=taskid, reason=reason, *args, **kwargs
        )


class NoTasksError(TaskError):
    """Thrown if tasks are requested, but there are none"""

    def __init__(self, *args, **kwargs):
        reason = "There are no tasks in the database."
        super(NoTasksError, self).__init__(reason=reason, *args, **kwargs)


class MissingImportError(ImportError):
    """Thrown if a library is missing."""

    def __init__(self, name, reason, *args, **kwargs):
        super(MissingImportError, self).__init__(*args, **kwargs)
        self.name = name
        self.reason = reason

    def __str__(self):
        return "{} {}.".format(self.name, self.reason)


class NotSupportedError(NotImplementedError):
    """Thrown if functionality isn't supported, and not implemented."""

    def __init__(self, reason, *args, **kwargs):
        super(NotSupportedError, self).__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        return self.reason


class UnrecognizedTargetError(ValueError):
    """Thrown if an unrecognized target is given for an action"""

    def __init__(self, name, reason="", *args, **kwargs):
        super(UnrecognizedTargetError, self).__init__(*args, **kwargs)
        self.name = name
        self.reason = reason

    def __str__(self):
        return "Unrecognized target {} {}.".format(self.name, self.reason)


class UnrecognizedExecutorError(UnrecognizedTargetError):
    """Thrown if an unrecognized executor is asked for"""

    def __init__(self, name, reason="is not a known executor", *args, **kwargs):
        super(UnrecognizedExecutorError, self).__init__(
            name=name, reason=reason, *args, **kwargs
        )


class OutputParsingError(ValueError):
    """Thrown if an output cannot be correctly parsed"""

    def __init__(self, reason="", *args, **kwargs):
        super(OutputParsingError, self).__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        return self.reason


class MissingDatabaseString(RuntimeError):
    """Thrown if a database string is required and not provided"""

    def __init__(self, reason=None, *args, **kwargs):
        super(MissingDatabaseString, self).__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        return (
            self.reason
            or "A database url must be defined to use a relational database. Set with qme config --database"
        )


class DatabaseStringFormatError(RuntimeError):
    """Thrown if database prefix is not supported"""

    def __str__(self):
        return (
            "Database must start with sqlite, filesystem, mysql+pymysql, or postgres."
        )
