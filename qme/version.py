"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

__version__ = "0.0.14"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "qme"
PACKAGE_URL = "http://www.github.com/vsoch/qme"
KEYWORDS = "python,dashboard,jobs,actions"
DESCRIPTION = "job submission and dashboard library"
LICENSE = "LICENSE"

################################################################################
# Global requirements


INSTALL_REQUIRES = ()

APP_REQUIRES = (
    ("Flask", {"min_version": "1.0.2"}),
    ("Flask-SocketIO", {"min_version": "3.1.2"}),
    ("flask-restful", {"min_version": "0.3.8"}),
    ("gevent-websocket", {"min_version": "0.10.1"}),
)

DATABASE_REQUIRES = (("sqlalchemy", {"min_version": None}),)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)


ALL_REQUIRES = INSTALL_REQUIRES + DATABASE_REQUIRES + APP_REQUIRES
