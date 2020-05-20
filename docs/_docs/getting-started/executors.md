---
title: Executors
category: Getting Started
permalink: /getting-started/executors/index.html
order: 4
---

As executor in the context of QuemeMe is a controller that will handle parsing of a command line (terminal)
command. Any executor must ensure that:

 - appropriate metadata is collected 
 - the command is run
 - relevant actions are exposed

This section will give an overall review of executors, including global (base) metadata,
and executor-specific details.

## The Executor base

All executors should be derived from the [ExecutorBase](https://github.com/vsoch/qme/blob/master/qme/main/executor/base.py#L74) class that will ensure that each one exposes the needed functions. Each executor also has it's own view under [app/templates](https://github.com/vsoch/qme/tree/master/qme/app/templates) that renders a page specific to it for the dashboard (under development). You should reference the class to see the functions that are required and conditions for each.

## Executors

### Base

Each executor must expose the following metadata:

 - **pwd**: the present working directory where the command was run
 - **command**: the command that was run
 - **user**: the user that ran the command
 - **status**: the status of the operation. Since most basic commands save the first time upon completion, the status is usually complete, however this is subject to change. This must be one of "complete" "cancelled" or "running" or None.

The only metadata shown on the table (front) page of the dashboard is these common attributes.
For the filesystem database, since we'd need to read many separate files, we just show
the executor type and unique id. The user must click on any particular execution to see
the full details.

### Shell

The "shell" executor is the default that will take any command that doesn't match a previous
regular expression, and the executor will run the command, parse output and error streams, and then
provide a result object with the following metadata:

 - **output**: the output stream of running the command
 - **error**: the error stream of running the command
 - **returncode**: the returncode from running the command
 - **pid**: the pid of the child process.

This means that it doesn't have a specific match string or actions beyond the basic that are
provided for any command (delete, view, and re-run). The matching [dashboard]({{ site.baseurl }}/getting-started/dashboard/index.html#shell) interface is also optimized to show and search this information, mainly the command and any output or error. An example shell run might look like:

```bash
$ qme run echo "hello moto"
```
```bash
$ qme get
Database: sqlite
{
    "executor": "shell",
    "uid": "shell-eab1fcff-d8b8-497a-bb7b-c758b23ff697",
    "data": {
        "pwd": "/home/vanessa/Desktop/Code/qme",
        "user": "vanessa",
        "timestamp": "2020-05-20 16:47:47.955877",
        "output": [
            "hello moto\n"
        ],
        "error": [],
        "returncode": 0,
        "command": [
            "echo",
            "hello moto"
        ],
        "status": "complete",
        "pid": 15048
    },
    "command": "echo hello moto"
}
```

There are no specific environment variables for shell, beyond the default, nor any actions.

### Slurm

The "slurm" executor is intended for using sbatch to run slurm jobs, sacct to check
on status, and scancel to cancel. Since the slurm executor is a subclass of shell
it exposes the same metadata. 

```bash

```

#### Actions

Actions include the following:

  - **status**: Get a status dictionary, with a default format string set by QueueMe
  - **output**: Get the output file output, if it exists. You should set `--out` or leave unset.
  - **error**: Get the error file output, if it exists. You should set `--err` or leave unset. 
  - **cancel**: cancel a job that was run with scancel

For output and error files, you can either leave unset (to use a default) or set `--out` or `--err` to
be read by QueueMe. SBATCH directives are not currently parsed.


You might next want to learn about the interactive [dashboard]({{ site.baseurl }}/getting-started/dashboard/).
