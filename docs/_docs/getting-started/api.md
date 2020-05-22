---
title: Application Programming Interface
category: Getting Started
permalink: /getting-started/api/index.html
order: 8
---

Let's say that you have a container running, and it serves as a base to run
scripts for your scientific analysis. You use QueueMe to run an [interactive dashboard](../dashboard/)
and that's great, but you really need programmatic access to the outputs. How might you do that?

## The QueueMe API

The dashboard also exposes a simple Restful API to the database! After you
start the dashboard:

```bash
$ qme start
```

If you look at the bottom of the table, there is a small link to view the tasks api.

![../img/api/dashboard.png](../img/api/dashboard.png)

The first page you go to is for all tasks, and from there you can navigate to a
particular taskid that is listed. You can browse to any of the `/api` endpoints to see all tasks, or a specific task.
There are currently just two simple functions for this:

 - [List all Tasks](#list-tasks)
 - [List Executor Tasks](#list-executor-tasks)
 - [Get a Task by Identifier](#get-task)


<a id="list-tasks">
##  List Tasks

The default view (when you click API or go to `/api/tasks` is to see a listing of tasks:

![../img/api/tasks.png](../img/api/tasks.png)

<a id="list-executor-tasks">
##  List Executor Tasks

If you adjust the url (`/api/tasks/executor/<name>`) to specify a particular executor, you'll see only those executor's tasks.

![../img/api/executor-tasks.png](../img/api/executor-tasks.png)

Since all of our tasks use the shell executor, these two lists happen to be the same.

<a id="get-task">
##  Get a Task by Taskid

Finally, to see any specific task (and it's metadata) you can generally go to `/api/tasks/<taskid>`

![../img/api/get-task.png](../img/api/get-task.png)

If you'd like to see any other endpoints added, please [open an issue]({{ site.baseurl }}/{{ site.repo }}/issues).
