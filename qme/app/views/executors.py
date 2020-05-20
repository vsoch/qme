"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import Flask, render_template
from flask_socketio import emit

from qme.app.server import app, socketio
from qme.defaults import QME_SOCKET_UPDATE_SECONDS


## Executor Views


@app.route("/executor/<taskid>")
def shell_executor(taskid):

    # TODO: return executor template based on task.executor.name
    task = app.queue.get(taskid)
    return render_template(
        "executors/shell.html", task=task.load(), database=app.queue.database
    )
