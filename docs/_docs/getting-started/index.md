---
title: Introduction
category: Getting Started
permalink: /getting-started/index.html
order: 1
---

You should first [install]({{ site.baseurl }}/install/) qme.
This will place the executable `qme` in your bin folder, which is the client
for running tasks, starting the interface, or otherwise interacting with your queue.

## Getting Started

### Introduction

 - [How does it work?](#how-does-it-work): How does qme work?
 - [Concepts](#concepts): What are common qme concepts?

### Setup

 - [Configuration](configure/) your qme install, for example, choosing a database backend.
 - [Environment](environment/) variables can be set to control functionality.

### Usage

 - [Commands](commands/) including run, re-run, list (ls), get, and others.
 - [Executors](executors/) are parsers for the commands that you run to create tasks.
 - [Dashboard](dashboard/) to better interact with and manage your tasks.
 - [Actions](actions/) are defined per executors, and can be called from command line or sometimes interface.
 - [Containers](containers/) including Docker, or more likely important, Singularity.
 - [API](api/) the dashboard also exposes an application programming interface for your tasks

<a id="#how-does-it-work">
### How does it work?

As we've [mentioned]({{ site.baseurl }}/index.html), QueueMe (or on the command line, qme) 
is a jobs queue and dashboard generation tool that can be used
to specify executors (entities that run jobs) and actions for them. You can
use qme only on the command line, or if desired, via an interactive web dashboard.
The basic workflow of QueueMe looks something like this:

```
                                             +-------+
                                             |       |
                                         +-->+ shell |
                                         |   |       |
                                         |   +-------+                     +--> qme clear...
                                         |                                 |
+-------------------+    +----------+    |   +-------+    +------------+   +--> qme get...
|                   |    |          |    |   |       |    |            |   |
|  qme run command  +--->+ executor +------->+ slurm |--->| database   +---+--> qme ls...
|                   |    |          |    |   |       |    |            |   |
+-------------------+    +----------+    |   +-------+    +------------+   +--> qme rerun...
                                         |       .                         |
                                         |       .                         +--> qme search...
                                         |   +-------+                     |
                                         |   |       |                     +--> qme start...
                                         +-->+ other |
                                             |       |
                                             +-------+

```

In the above diagram, we start with a qme run command, and it get's parsed by a particular
executor (e.g., slurm, shell, or other). The executor interacts with our database of choice
(filesystem, sqlite, mysql, or postgres) to save custom metadata for the command (e.g,
output, error, return code, present working directory, etc. for shell). The
user can then query qme to get, list, re-run, or clear a set of tasks or a particular task result, 
or generally list all tasks or open an interactive web interface to do the same.

The dashboard will show a table of results:

![img/dashboard/prototype.png](img/dashboard/prototype.png)

where you can click one to see it's executor-specific web interface (for example,
a shell executor is optimized to show output, error, metadata, and the command at
the top:

![img/executors/shell.png](img/executors/shell.png)

and then makes it easy search output. A search box at the top will highlight results
in yellow that match the user search:

![img/executors/shell-search.png](img/executors/shell-search.png)

The interface pages are automatically updated (without refreshing the page) by way of
using [web sockets](https://python-socketio.readthedocs.io/en/latest/intro.html), along
with [Vue.js](https://vuejs.org/) and [Flask](https://flask.palletsprojects.com/en/1.1.x/).

<a id="#concepts">
### Concepts

The following concepts might not be specific to qme, but are defined as the following
in the context of qme:

**executor**

You can think of an executor as the controller that will handle parsing of a command line (terminal)
command, and ensuring that:

 - appropriate metadata is collected 
 - the command is run
 - relevant actions are exposed

**dashboard**

Is a Flask application that comes with qme, exposed via `qme start`, that provides
an table to manage and otherwise interact with tasks.


**database**

A database is the backend database used by QME to store your tasks. The default (and dummy)
database is the filesystem, which is good if you want to briefly test out QueueMe but
not use extensively. For most use cases, sqlite is recommended as it supports display
or more information and easier search. You can easily install the sqlachemy database
dependency and then specify using sqlite for your configuration by doing the following:

```bash
$ pip install -e .[all]         # local install from repository
$ pip install -e qme[all]       # install from pypi
$ qme config --database sqlite
```

## Licenses

This code is licensed under the Mozilla, version 2.0 or later [LICENSE](LICENSE).

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
