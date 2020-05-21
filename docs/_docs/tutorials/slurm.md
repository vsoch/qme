---
title: Configuration
category: Tutorials
permalink: /tutorials/slurm/index.html
order: 2
---

## Setup

Let's say we just shelled into our research cluster, and we installed qme:

```bash
$ pip install qme[all]
```

We would first want to set up a more robust filesystem database, sqlite,
and we can do that like this:

```bash
$ qme config --database sqlite
Creating QueueMe home at /home/users/vsochat/.qme.
Configuration saved with database sqlite
```

This command creates our QME_HOME at $HOME/.qme:

```bash
$ tree $HOME/.qme
/home/users/vsochat/.qme
└── config.ini
```

As we already know, we call this the [environment variable](../environment/) `QME_HOME`.

## Run a Command

Let's jump right in and run a command for a job! Let's say we have a submission script,
and it's rather stupid and terrible, `run_job.sh`

```bash
#!/bin/bash

echo "HELLO WORLD"
```

We would normally submit this to run with something like:

```bash
$ sbatch --partition owners --time 00:00:10 run_job.sh
```

With qme, however, we add a `qme run` prefix to that:

```bash
$ qme run sbatch --partition owners --time 00:00:10 run_job.sh
```

And then get the job in our Queue:

```bash
]$ qme get
Database: sqlite
{
    "executor": "slurm",
    "uid": "slurm-4e84f806-6787-42e2-8ece-00646328df7f",
    "data": {
        "pwd": "/home/users/vsochat",
        "user": "vsochat",
        "timestamp": "2020-05-21 08:17:06.109921",
        "output": [
            "Submitted batch job 940840\n"
        ],
        "error": [],
        "returncode": 0,
        "command": [
            "sbatch",
            "--partition",
            "owners",
            "--time",
            "00:00:10",
            "run_job.sh"
        ],
        "status": "complete",
        "pid": 150185,
        "jobid": "940840",
        "outputfile": "/home/users/vsochat/slurm-940840.out",
        "errorfile": "/home/users/vsochat/slurm-940840.err"
    },
    "command": "sbatch --partition owners --time 00:00:10 run_job.sh"
}
```

If you want any help, please don't be afraid to [reach out](https://github.com/{{ site.repo }}/issues).
