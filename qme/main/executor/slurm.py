"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys
import re

from qme.logger import bot
from .shell import ShellExecutor


class SlurmExecutor(ShellExecutor):
    """A slurm executor parses an srun command and exposes options for getting
       a job status.
    """

    name = "slurm"
    matchstring = "^sbatch"

    def __init__(self, taskid=None, command=None):
        super().__init__(taskid, command)
        self.jobid = None
        self.actions = {
            "status": self.action_get_status,
            "output": self.action_get_output,
            "error": self.action_get_error,
            "outputs": self.action_get_outputs,
            "cancel": self.action_cancel,
        }

    def execute(self, cmd=None):
        """Execute a system command and return output and error. Execute
           should take a cmd (a string or list) and execute it according to
           the executor. Attributes should be set on the class that are
           added to self.export. Since the functions here are likely needed
           by most executors, we create a self._execute() class that is called
           instead, and can be used by the other executors.
        """
        self._execute(cmd)
        if self.returncode == 0:

            import IPython

            IPython.embed()

            # Find the job id, and any --out or --error files
            match = re.search("[0-9]+", self.out[0])
            if not match:
                bot.exit(f"Unable to derive job id from {self.out}")
            self.jobid = match.group()

            # Get output file, or default to $PWD/slurm-<jobid>
            self.errorfile = os.path.join(self.pwd, "slurm-%s.err" % self.jobid)
            self.outputfile = os.path.join(self.pwd, "slurm-%s.out" % self.jobid)

            match = re.search("(--out|-o) (?P<output>[^\s-]+)", self.command)
            if match:
                self.outputfile = match.groups("output")[1]

            match = re.search("(--err|-e) (?P<error>[^\s-]+)", self.command)
            if match:
                self.errorfile = match.groups("error")[1]

    # Actions

    def action_get_status(self):
        """Get the status with squeue, given a jobid
        """
        if self.jobid:
            capture = self.capture(["squeue", "--job", self.jobid])

        self.pid = capture.pid
        self.returncode = capture.returncode
        self.out = capture.output
        self.err = capture.error
        self.status = "complete"
        return (self.out, self.err)

    def action_get_error(self):
        """Get error stream, if the file exists.
        """
        pass

    def action_get_output(self):
        """Get just output stream, if the file exists.
        """
        pass

    def action_get_outputs(self):
        """Get *both* output and error streams, if files exist.
        """
        pass

    def action_cancel(self):
        """Cancel a job if there is a jobid
        """
        pass
