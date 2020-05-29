---
title: Commands
category: Getting Started
permalink: /getting-started/commands/index.html
order: 3
---

This section includes commands for QueueMe, and will be expanded as the library
is developed.

 - [Run](#run) a task that will be handled by a QueueMe executor.
 - [Get](#get) a previously run task, either the last one, or by taskid
 - [List](#list) all tasks or tasks specific to an executor
 - [Clear](#clear) a single task, all tasks for an executor, or all tasks.
 - [Search](#search) across your tasks to find a particular one.
 - [Start](#start) an interactive dashboard to see and manage tasks.

<a id="run">
## Run

You can currently run a basic terminal command (one that is executed and has error,
output, and a return code) like the following:

```bash
$ qme run ls $PWD
DATABASE: filesystem
[shell-5b8a154e-5178-4b1c-811c-d493d4349f1f][returncode: 0]
```

The command is so quick that it gives you the result immediately. In the above,
we see the executor (shell) along with the unique id (the following uuid), 
and the full command (to list the expanded $PWD) and the return code 0. 
If you want to add a message (annotation) to store with the task and be used
for search, add `-m/--message` to your run:

```bash
qme -m "This is a listing for the thing" run ls $PWD
```

There is one special case, the argument --help, which if run without
thinking, will be parsed by the client and print the get help:

```bash
$ qme run singularity --help
usage: qme run [-h] [cmd [cmd ...]]

positional arguments:
  cmd         The command to parse. If --help needed, should be fully quoted.

optional arguments:
  -h, --help  show this help message and exit
```

To correctly run this command, we should quote it:

```bash
$ qme run "singularity --help"
Database: sqlite
[shell-7fe77fee-4970-48bd-a11d-70d750ca62d5][returncode: 0]
```

<a id="get">
## Get 

Once we know a task id (`shell-5b8a154e-5178-4b1c-811c-d493d4349f1f` for the above)
we likely want to get a summary of it. We can do that with `qme get`, which 
expects a task id.

```bash
$ qme get shell-e8098ce8-bb9d-4193-bcdf-fc3dc221ca0c
Database: sqlite
{
    "executor": "shell",
    "uid": "shell-e8098ce8-bb9d-4193-bcdf-fc3dc221ca0c",
    "data": {
        "pwd": "/home/vanessa/Desktop/Code/qme",
        "user": "vanessa",
        "timestamp": "2020-05-21 10:35:10.894684",
        "output": [
            "build\n",
            "CHANGELOG.md\n",
            "dist\n",
            "Dockerfile\n",
            "docs\n",
            "LICENSE\n",
            "MANIFEST.in\n",
            "paper\n",
            "qme\n",
            "qme.egg-info\n",
            "README.md\n",
            "setup.cfg\n",
            "setup.py\n",
            "tests\n"
        ],
        "error": [],
        "returncode": 0,
        "pid": 1639,
        "cmd": [
            "ls"
        ],
        "status": "complete"
    },
    "command": "ls"
}
```

Actually, we can get the last task run (the same as above) just with qme get.

```bash
$ qme get
```

It will retrieve the last updated entry in the database across executors.

<a id="list">
## List

For the command line, you can easily list tasks. For the filesystem database,
since we would need to read in several json files, the listing just shows the
task ids. If you do a general list with `qme ls`, it will show all task ids:

```bash
$ qme ls
DATABASE: filesystem
1  shell-7a2f5e23-27ef-49eb-a6a6-896ddc690117
2  shell-84f90411-a53e-4d40-92b0-706e5ddfa3b9
3  shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a
4  shell-542e11ef-a1d1-47ce-90a7-40fc7829d29f
5  shell-0f85a77f-f442-46b1-88b1-7d55303b2119
6  shell-5a9e4413-b25d-4dca-826f-f9f8b27abf50
7  shell-2e65e814-388d-4617-bf89-ef307ba6fa40
8  shell-c07e9279-eee7-4778-9212-4ac617a6082e
9  shell-bcaae4db-2970-4674-9800-376c891c1454
10 shell-38307314-9825-435b-8fb6-6d37b3427a7b
11 shell-ad239488-2a27-47b9-8225-da227625e913
```

The above tasks are for the shell executor, which is the default if no special
executor is selected. You could explicitly state this like:

```bash
$ qme ls shell
DATABASE: filesystem
1  shell-7a2f5e23-27ef-49eb-a6a6-896ddc690117
2  shell-84f90411-a53e-4d40-92b0-706e5ddfa3b9
3  shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a
4  shell-542e11ef-a1d1-47ce-90a7-40fc7829d29f
5  shell-0f85a77f-f442-46b1-88b1-7d55303b2119
6  shell-5a9e4413-b25d-4dca-826f-f9f8b27abf50
7  shell-2e65e814-388d-4617-bf89-ef307ba6fa40
8  shell-c07e9279-eee7-4778-9212-4ac617a6082e
9  shell-bcaae4db-2970-4674-9800-376c891c1454
10 shell-38307314-9825-435b-8fb6-6d37b3427a7b
11 shell-ad239488-2a27-47b9-8225-da227625e913
```

If you use a more robust relational database (so we wouldn't need to load
many json files to list) you can get the commands along with the executor
and id:

```bash
$ qme ls
Database: sqlite
1  shell-04b40eac-03bc-4074-9e8e-f2d3eb3806f5	ls
2  shell-2c789017-5828-44ca-a49d-c5912800c044	ls
3  shell-c51898a8-884b-445c-86d5-e3811605584b	whoami
```

<a id="clear">
## Clear

If you want to delete a task, just use clear with it's unique id:

```bash
$ qme clear shell-84f90411-a53e-4d40-92b0-706e5ddfa3b9
DATABASE: filesystem
This will delete task shell-84f90411-a53e-4d40-92b0-706e5ddfa3b9, are you sure? [n]|y: y
shell-84f90411-a53e-4d40-92b0-706e5ddfa3b9 has been removed.
```

You can also remove an entire executor:

```bash
$ qme clear shell
DATABASE: filesystem
This will delete all executor shell tasks, are you sure? [n]|y: n
```

or all tasks in the database:

```bash
$ qme clear
DATABASE: filesystem
This will delete all tasks, are you sure? [n]|y: n
```

Each time you'll be asked for a confirmation first, in case the command was 
run in error.

<a id="rerun">
## Rerun

You can re-run any task, also based on it's taskid. A re-run will load the 
previous command, change to a different directory (if set) and then
re-run the command. The result will be stored under the  (updated) taskid.
Here is a quick example of showing an older task (run before some of the library
was developed) and then using re-run, and showing that the task is updated.
First, here is the original task:

```bash
$ qme get shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a
DATABASE: filesystem
{
    "executor": "shell",
    "command": [
        "ls"
    ],
    "uid": "shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a"
}
```

Now we re-run it:

```bash
$ qme rerun shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a
DATABASE: filesystem
[shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a][returncode: 0]
```

And finally, we see that the task is updated.

```bash
$ qme get shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a
DATABASE: filesystem
{
    "executor": "shell",
    "command": [
        "ls"
    ],
    "uid": "shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a",
    "data": {
        "pwd": "/home/vanessa/Desktop/Code/qme",
        "output": [
            "build\n",
            "CHANGELOG.md\n",
            "dist\n",
            "docs\n",
            "LICENSE\n",
            "MANIFEST.in\n",
            "paper\n",
            "qme\n",
            "qme.egg-info\n",
            "README.md\n",
            "setup.cfg\n",
            "setup.py\n",
            "tests\n"
        ],
        "error": [],
        "returncode": 0
    },
    "command": "ls"
}
```

You can also rerun the last touched task without needing to specify the identifier.

```bash
$ qme rerun
```

And akin to run, if you want to add a message (to update the existing) you can
do that too:


```bash
qme -m "This is a listing for the thing" rerun
```


<a id="search">
## Search

Let's say that we run a bunch of tasks, and either the command or result has a term
of choice that we want to find again. 

```bash
$ qme run echo Hello Moto
$ qme run echo Hello Another Moto
```

We might then want to search for these commands! For a sanity check, let's make
sure we know their taskids in advance:

```bash
$ qme ls | grep Moto
2  shell-de58f61b-81da-467c-981c-497f7ae8556b	echo Hello Moto
3  shell-c231699a-4c3e-43f0-961f-2829d16d588c	echo Hello Another Moto
```

Aside from listing and using grep, we can just use `qme search`.

```bash
$ qme search moto
Database: sqlite
1  shell-de58f61b-81da-467c-981c-497f7ae8556b	2020-05-22 17:47:37	echo Hello Moto
2  shell-c231699a-4c3e-43f0-961f-2829d16d588c	2020-05-22 17:47:45	echo Hello Another Moto
```

Notice that the search is case insensitive. We get back the taskid (that is prefixed with
the executor) along with the timestamp and the command itself. Tasks with matches in
some part of the metadata (e.g., a string in the output or error) would be included too.
Since search takes advantage of using a relational (or sqlite) database,
the filesystem database is not supported.

```bsah
$ qme config --database filesystem
Configuration saved with database filesystem
$ qme search moto
Database: filesystem
Search is only supported for relational databases.
```

<a id="start">
## Start

The qme start command will open a web interface with an interactive table
for your tasks. 

```bash
$ qme start
```

You can run it in debug mode:

```bash
$ qme start --debug
```

or further customize the port or hostname

```bash
$ qme start --port 8000 --host 0.0.0.0
```

For each, you can specify a particular action (e.g., delete or re-run)
or click on it for further details.  See the [dashboard]({{ site.baseurl }}/getting-started/dashboard/) 
documentation page for more details.
