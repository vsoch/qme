---
title: Queue Me
permalink: /
---

> What is QueueMe (qme)?

QueueMe (on the command line, qme) is a jobs queue and dashboard generation tool that can be used
to specify executors (entities that run jobs) and actions for them. You can
use qme only on the command line, or if desired, via an interactive web dashboard.
In both cases, you can customize using (or not using) a database, along with 
setting executor-specific arguments that might be available (for example, an sacct
format string can be set to override the default to determine the output of
the "status" action for the slurm executor. 
The dashboard (and it's dependencies) are not required for using the base library.

<a id="#how-does-it-work">
> How does it work?

After you [install]({{ site.baseurl }}/install/) qme, you can run a task, for example,
listing files in the present working directory.

```bash
$ qme run ls
```

you can then get the task via the command line:

```bash
$ qme get
```

or list all tasks for a particular executor (e.g., shell):

```bash
$ qme ls shell
```

or search across all metadata and task commands for a query of interest:

```bash
$ qme search moto
```

or just list all tasks

```bash
$ qme ls
```

and then get a specific task id (output shown this time):

```bash
$ qme get shell-a561702d-404e-4fb2-be27-57496b32ac46
DATABASE: filesystem
{
    "executor": "shell",
    "uid": "shell-a561702d-404e-4fb2-be27-57496b32ac46",
    "data": {
        "pwd": "/home/vanessa",
        "user": "vanessa",
        "output": [
            "vanessa\n"
        ],
        "error": [],
        "returncode": 0,
        "command": [
            "whoami"
        ],
        "status": "complete",
        "pid": 3110
    },
    "command": "ls"
}
```

You can also clear:

```bash
# clear all tasks in the database
$ qme clear 

# clear tasks for the shell executor
$ qme clear shell

# delete a specific task based on taskid
$ qme clear shell-a561702d-404e-4fb2-be27-57496b32ac46
```

search (coming soon), configure, or start an interactive interface:

```bash
$ qme search <query>
$ qme config --database sqlite
$ qme start
```

The interactive session means opening up a web interface that shows an interactive
table that updates automatically with changed or new tasks via web sockets.

> What are intended use cases for qme?

QueueMe is intended to help you organize your many command line tasks, which means:

 - remembering the commands that you ran
 - being able to request actions (e.g., ping for a status)
 - being able to easily search or get metadata about a particular command

More specifically, qme provides a layer of reproducibility to your terminal usage,
because instead of spitting out commands that you do not remember or doing a grep
to search your linux history, you instead store the commands in a database.
The commands are parsed to matched executors of interest (e.g. slurm would
match srun and expose commands to interact with your submission) and if no executor is matched,
it's treated as a standard Shell command (shell capture standard output, error, and return codes).

> What is an executor?

An executor is a specific parser for a command, which is determined based on 
regular expressions to match the command. For example, a "datalad" parser might match
any command given to `qme run` that starts with "datalad" and a "slurm" parser might match
anything that starts with `srun`  The parser can then further
parse the specific command. Along with parsing the command, the executor can then:

 - capture specific metadata important to know (e.g., the present working directory or username)
 - further check the command for correctness, and tell the user how to improve or fix it if needed.
 - define custom actions to run for the command (e.g., a slurm executor would retrieve the job id and expose a status function to the user)
 - define a custom interface for displaying the actions and metadata parsde.

Executors can be created for general command line tools, serving as a wrapper:

```bash
$ qme run qsub myscript.sh
$ qme run ls
```

or even created for custom use cases that don't require a command line executable at all! For example,
we might define a MadLibs executor that takes an input file with a list of words, and generates
a random MadLib for the user.

```bash
$ qme run madlib mywords.txt
```

That's the cool part about qme - there is huge freedom in defining what an executor is, what
an executor can do, and what user interface is exposed for the results.

> Where do I go from here?

A good place to start is the [getting started]({{ site.baseurl }}/getting-started/) page,
which has links for getting started with writing tests, running tests, and many examples.
