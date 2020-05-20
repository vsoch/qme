---
title: Creating an Executor
category: Tutorials
permalink: /tutorials/create-executor/index.html
order: 3
---

## Organization

Each executor has it's own module file, which is located under "qme/main/executors."
For example, here we see a structure that provides a base, shell, and slurm executor:

```
$ tree qme/main/executor/
qme/main/executor/
├── base.py
├── __init__.py
├── shell.py
└── slurm.py
```
In the `__init__.py` file, there is basic logic to run a command over a number
of regular expressions, and to return the executor class that matches.
Here is a basic example with two executors, shell and slurm, early in the library
development:

```python
def matches(Executor, command):
    """Given a command, determine if it matches the regular expression
       that determines to use the executor or not. This applies to all
       executors except for the shell executor. This means that all non-shell
       classes need to have a matchstring defined.
    """
    if not hasattr(Executor, "matchstring"):
        raise NotImplementedError

    if isinstance(command, list):
        command = " ".join(command)
    return not re.search(Executor.matchstring, command) == None


def get_executor(command=None):
    """get executor will return the correct executor depending on a command (or
       other string) matching a regular expression. If nothing matches, we 
       default to a shell executor. Each non-shell executor should expose
       a common "matches" function (provided by the base class) that will
       handle parsing the command (a list) to a single string, and checking
       if it matches a regular expression.
    """
    # Slurm Executor
    if matches(SlurmExecutor, command):
        return SlurmExecutor(command=command)

    # Default is standard shell command
    return ShellExecutor(command=command)
```

You'll also notice each executor type is imported at the top of the file:

```python
from .shell import ShellExecutor
from .slurm import SlurmExecutor
```

For this tutorial we will discuss creation of the Slurm Executor. You will need to:

 1. Create a file `<executor-name>.py` in the qme/main/executors folder.
 2. Define it's functionality (optionally being subclass to a parent like the ShellExecutor), along with a name and matchstring
 3. Import the executor into the `__init__.py`
 4. Add any custom actions that you executor exposes
 5. Write tests for your executor

The following sections will discuss these points.

## 1. Create your Executor File

The first thing to do is decide if your executor warrants a parent class. For
most terminal commands, a ShellExecutor base would be most appropriate, as it
already handles parsing the command, and collecting output, error, and a return
code. For example, below we see importing the `ShellExecutor` into a new file,
`slurm.py`, and instantiating the `execute` function that will call the
already existing shell's _execute that will run the command. Also notice
that we have chosen a `matchstring`, a class variable, that will determine
that we have an sbatch command.

```python
from .shell import ShellExecutor


class SlurmExecutor(ShellExecutor):
    """A slurm executor parses an srun command and exposes options for getting
       a job status.
    """

    name = "slurm"
    matchstring = "^sbatch"

    def execute(self, cmd=None):
        """Execute a system command and return output and error. Execute
           should take a cmd (a string or list) and execute it according to
           the executor. Attributes should be set on the class that are
           added to self.export. Since the functions here are likely needed
           by most executors, we create a self._execute() class that is called
           instead, and can be used by the other executors.
        """
        self._execute(cmd)
        # Do custom parsing of self.out, self.err, self.returncode here
```

At this point you might bring it onto a cluster, add an `IPython.embed()` in the
execute function, and interactively develop and write the code. You would
clone your feature branch, install qme from it, and then run a command
that should match:

```bash
$ git clone -b add/slurm-executor git@github.com:vsoch/qme.git
$ pip install -e .[all]
$ which qme
$ qme run sbatch --partition normal --time 00:00:10 run_job.sh
```

If you want some help with your executor, please don't be afraid to [reach out](https://github.com/{{ site.repo }}/issues).
