"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask_socketio import SocketIO
from flask import Flask

from qme.logger import bot
from qme.defaults import QME_HOSTNAME

import logging
import os


class QueueMeServer(Flask):
    def __init__(self, *args, **kwargs):
        super(QueueMeServer, self).__init__(*args, **kwargs)


app = QueueMeServer(__name__)
app.config.from_object("qme.app.config")

# turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

from qme.app.views import *
from qme.app.api import *


def start(port=5000, debug=True, queue=None, host=None):
    """Start can be invoked when this file is executed (see __main__ below)
       or used as a function to programmatically start a server. If started
       via qme view, we can add the queue to the server. If you want to change
       the hostname, set the environment variable QME_HOSTNAME or set on command
       line with qme start.
    """
    host = host or QME_HOSTNAME
    bot.info(f"QueueMe: running on http://{host}:{port}")

    # If the user doesn't specify a queue, use default
    if not queue:
        from qme.main import Queue

        queue = Queue()

    # Customize the logger to log to the app folder
    file_handler = logging.FileHandler(os.path.join(queue.config_dir, "dashboard.log"))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

    # Add the queue to the server
    app.queue = queue
    socketio.run(app, port=port, debug=debug, host=host)


# This is how the command line version will run
if __name__ == "__main__":
    start()
