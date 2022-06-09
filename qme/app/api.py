"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import flask
from flask_restful import Resource, Api
from qme.app.server import app


def list_tasks(executor=None):
    """A shared function to list one or more tasks, optionally for an executor,
    and return a json list to serialize to the api view
    """
    tasks = []
    url = flask.request.host_url
    for i, task in enumerate(app.queue.list(executor)):
        tasks.append(
            {
                "taskid": task[0],
                "command": task[1],
                "html_url": "%sexecutor/%s" % (url, task[0]),
                "api_url": "%sapi/tasks/%s" % (url, task[0]),
            }
        )
    return tasks


class apiList(Resource):
    """display all tasks"""

    def get(self):
        return list_tasks()


class apiListExecutor(Resource):
    """display all tasks for an executor"""

    def get(self, executor):
        return list_tasks(executor)


class apiGet(Resource):
    """display a specific task
    :param taskid: id for a specific task
    """

    def get(self, taskid):
        task = app.queue.get(taskid)
        return task.export()


api = Api(app)
api.add_resource(apiList, "/api/tasks")
api.add_resource(apiGet, "/api/tasks/<string:taskid>")
api.add_resource(apiListExecutor, "/api/tasks/executor/<string:executor>")
