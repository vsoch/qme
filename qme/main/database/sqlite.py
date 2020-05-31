"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.main.database.relational import RelationalDatabase

import logging
import os
import sys

bot = logging.getLogger("qme.main.database.sqlite")


class SqliteDatabase(RelationalDatabase):
    """A SqliteDatabase writes to a qme.db file in $HOME/.qme. This is
       the suggested database backend for QueueMe, as it doesn't require anything
       beyond a filesystem and still allows for relational type queries.
    """

    database = "sqlite"

    def __init__(self, config_dir, config=None, **kwargs):
        """init for the filesystem ensures that the base folder (named 
           according to the studyid) exists.
        """
        database_file = kwargs.get("database_string", "qme.db") or "qme.db"

        # Derive database path, use default of qme.db if not provided
        db_path = os.path.join(config_dir, database_file)
        if not db_path.endswith(".db"):
            bot.error(
                f"Invalid database file for sqlite, {database_file} does not end in .db"
            )
            sys.exit(1)

        self.config = config
        self.db = "sqlite:///%s" % db_path
        self.create_database()
