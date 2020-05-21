---
title: Actions
category: Getting Started
permalink: /getting-started/actions/index.html
order: 6
---

Each executor can expose it's own custom actions, which in addition to the 
ability to run, re-run, or clear (see [commands](../commands/)), allow
a user to execute custom actions to get status updates or similar. Here
we will walk through a basic example for getting actions from within
Python, or from the command line.

## Command Line

First, let's run a command to launch a little script.

```bash
$ qme run sbatch --partition owners --time 00:00:10 run_job.sh
[slurm-02eecdcd-a6b2-4055-8fad-c94e846a0f26][returncode: 0]
```

To get actions for an executor, just run the `qme exec slurm` without any arguments,
where "slurm" is the name of the executor, and exec implies we want to execute an action.

```bash
$ qme exec slurm
1  status
2  output
3  error
4  cancel
```

Let's try getting a status, for our last task run (we don't need a task id or
an executor):

```bash
$ qme exec status
```

If we had needed to include the job identifier (if it wasn't the last job) we 
could have asked for it. Notice that the executor is provided with the taskid, so
we don't need to include it again.

```bash
$ qme exec slurm-02eecdcd-a6b2-4055-8fad-c94e846a0f26 status
```


## Python

Let's say that we create a Queue, and we use all the defaults.

```python
from qme.main import Queue
queue = Queue()
```

### 1. Run a Task
Now we want to run a command. Since the command will start with sbatch,
this will give us a slurm executor task back.

```python
task = queue.run("sbatch --partition owners --time 00:00:10 run_job.sh")
[slurm-8e70abab-fe8b-43cb-b108-b1b1da725cac][returncode: 0]
```

as a reminder, this would be equivalent to running

```bash
$ qme run sbatch --partition owners --time 00:00:10 run_job.sh
```

### 2. Inspect Metadata
on the command line. We could quickly get the current metadat with task.load:

```python
> task.load()
{'executor': 'slurm',
 'uid': 'slurm-8e70abab-fe8b-43cb-b108-b1b1da725cac',
 'data': {'pwd': '/home/users/vsochat',
  'user': 'vsochat',
  'timestamp': '2020-05-20 16:01:33.169770',
  'output': ['Submitted batch job 906448\n'],
  'error': [],
  'returncode': 0,
  'command': ['sbatch',
   '--partition',
   'owners',
   '--time',
   '00:00:10',
   'run_job.sh'],
  'status': 'complete',
  'pid': 127569},
 'command': 'sbatch --partition owners --time 00:00:10 run_job.sh'}
```

### 3. Get Actions
But actually, we aren't interested in the running command, we want to get the
status of the job, according to slurm. Or we might want output. Let's see what
actions our task executor exposes!

```python
task.executor.get_actions()                                                                             
['status', 'output', 'error', 'cancel']
```

#### 4. Run Actions

Cool! Let's get a status.

```python
> task.executor.run_action('status')
{'jobid': '906448',
 'jobname': 'run_job.sh',
 'partition': 'owners',
 'alloccpus': '1',
 'elapsed': '00:00:00',
 'state': 'PENDING',
 'exitcode': '0:0'}
```

We might also want to get output or error (if the job has been run and the files
exist). Here is what we see when it doesn't exist yet - it's presented as a list
of lines, when returned by the function.

```python
> task.executor.run_action('output')
['/home/users/vsochat/slurm-906448.err does not exist.\n']
```

When we get that the status is complete, we can try again:

```python
> task.executor.run_action('output')
['HELLO WORLD\n']
```

How boring!
