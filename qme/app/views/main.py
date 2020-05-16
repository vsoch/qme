"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from flask import Flask, render_template
from flask_socketio import emit

# from werkzeug import secure_filename
from qme.app.server import app, socketio
from qme.defaults import QME_SOCKET_UPDATE_SECONDS

from random import random
from time import sleep
from threading import Thread, Event

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()


def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    # infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = round(random() * 10, 3)
        socketio.emit("newnumber", {"number": number}, namespace="/test")
        socketio.sleep(5)


## Main Index View


@app.route("/")
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template("index.html")


## Updating database rows


def update_database():
    """A function to be run at some interval to update the qme database listing
    """
    while not thread_stop_event.isSet():

        # The data sent to the table depends on the database
        if app.queue.database == "filesystem":
            app.logger.debug("Detected filesystem database")
            rows = app.queue.list()
            print(rows)
            socketio.emit(
                "FSdatabase",
                {"rows": rows, "database": app.queue.database},
                namespace="/update",
            )
        socketio.sleep(QME_SOCKET_UPDATE_SECONDS)


@socketio.on("connect", namespace="/update")
def update_connect():
    # need visibility of the global thread object
    global thread
    app.logger.debug("Client connected")

    # Start the process to update the table
    app.logger.debug("Starting Thread")
    thread = socketio.start_background_task(update_database)


@socketio.on("disconnect", namespace="/update")
def update_disconnect():
    app.logger.debug("Client disconnected")
