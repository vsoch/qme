"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


class MissingEnvironmentVariable(RuntimeError):
    """Thrown if a required environment variable is not provided.
    """

    def __init__(self, varname, *args, **kwargs):
        super(MissingEnvironmentVariable, self).__init__(*args, **kwargs)
        self.varname = varname

    def __str__(self):
        return "Missing environment variable '{}' is required".format(self.varname)


class InvalidDatabaseFilename(RuntimeError):
    """Database filename is invalid (must end in .db
    """

    def __init__(self, filename, *args, **kwargs):
        super(InvalidDatabaseFilename, self).__init__(*args, **kwargs)
        self.filename = filename

    def __str__(self):
        return "Invalid database file for sqlite, '{}' does not end in .db".format(
            self.filename
        )


class DirectoryNotFoundError(FileNotFoundError):
    """Thrown if a directory is not found
    """

    def __init__(self, dirname, reason, *args, **kwargs):
        super(DirectoryNotFoundError, self).__init__(*args, **kwargs)
        self.dirname = dirname
        self.reason = reason

    def __str__(self):
        return "{} {}.".format(self.dirname, self.reason)


class MultipleTasksExistError(RuntimeError):
    """Thrown if multiple tasks exist.
    """

    def __init__(self, taskid, *args, **kwargs):
        super(MultipleTasksExistError, self).__init__(*args, **kwargs)
        self.taskid = taskid

    def __str__(self):
        return "More than one task found for {}.".format(self.taskid)


class TaskNotFoundError(RuntimeError):
    """Thrown if task does not exist.
    """

    def __init__(self, taskid, *args, **kwargs):
        super(TaskNotFoundError, self).__init__(*args, **kwargs)
        self.taskid = taskid

    def __str__(self):
        return "Cannot find task {}.".format(self.taskid)


class NoTasksError(RuntimeError):
    """Thrown if tasks are requested, but there are none
    """

    def __str__(self):
        return "There are no tasks in the database."


class MissingImportError(ImportError):
    """Thrown if a library is missing.
    """

    def __init__(self, name, reason, *args, **kwargs):
        super(MissingImportError, self).__init__(*args, **kwargs)
        self.name = name
        self.reason = reason

    def __str__(self):
        return "{} {}.".format(self.name, self.reason)


class YerAnIdiotHarryError(RuntimeError):
    """Thrown if task does not exist.
    """

    def __init__(self, name, *args, **kwargs):
        super(YerAnIdiotHarryError, self).__init__(*args, **kwargs)
        self.name = name

    def __str__(self):
        return "I can't believe you tried to do that, {}.".format(self.name)


class NotSupportedError(NotImplementedError):
    """Thrown if functionality isn't supported, and not implemented.
    """

    def __init__(self, reason, *args, **kwargs):
        super(NotSupportedError, self).__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        return self.reason


class UnrecognizedTargetError(RuntimeError):
    """Thrown if an unrecognized target is given for an action
    """

    def __init__(self, name, reason="", *args, **kwargs):
        super(UnrecognizedTargetError, self).__init__(*args, **kwargs)
        self.name = name
        self.reason = reason

    def __str__(self):
        return "Unrecognized target {} {}.".format(self.name, self.reason)


class UnrecognizedExecutorError(UnrecognizedTargetError):
    """Thrown if an unrecognized executor is asked for
    """

    def __init__(self, name, reason="is not a known executor", *args, **kwargs):
        super(UnrecognizedExecutorError, self).__init__(
            name=name, reason=reason, *args, **kwargs
        )


class OutputParsingError(RuntimeError):
    """Thrown if an output cannot be correctly parsed
    """

    def __init__(self, reason="", *args, **kwargs):
        super(OutputParsingError, self).__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        return self.reason


class MissingDatabaseString(RuntimeError):
    """Thrown if a database string is required and not provided
    """

    def __init__(self, reason=None, *args, **kwargs):
        super(MissingDatabaseString, self).__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        return (
            self.reason
            or "A database url must be defined to use a relational database. Set with qme config --database"
        )


class DatabaseStringFormatError(RuntimeError):
    """Thrown if tasks are requested, but there are none
    """

    def __str__(self):
        return (
            "Database must start with sqlite, filesystem, mysql+pymysql, or postgres."
        )
