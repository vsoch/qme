"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys
import re

from qme.utils.file import read_file
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
        """Get the status with squeue, given a jobid. This returns information
           for the job that is based on a format string, default looks like:

		{'jobid': '904366',
		 'jobname': 'run_job.sh',
		 'partition': 'owners',
		 'alloccpus': '1',
		 'elapsed': '00:00:00',
		 'state': 'PENDING',
		 'exitcode': '0:0'}
        """
        fmt = self.get_setting(
            "sacct_format", "jobid,jobname,partition,alloccpus,elapsed,state,exitcode"
        )
        if self.jobid:
            capture = self.capture(
                ["sacct", "--job", self.jobid, "--format=%s" % fmt, "--noheader"]
            )
            values = {}
            output = [x for x in capture.output[0].strip().split(" ") if x]
            for i, varname in enumerate(fmt.split(",")):
                values[varname] = output[i]
            return values

    def action_get_output(self):
        """Get error stream, if the file exists.
        """
        if os.path.exists(self.outputfile):
            return read_file(self.outputfile)
        return ["%s does not exist.\n" % self.outputfile]

    def action_get_error(self):
        """Get just output stream, if the file exists.
        """
        if os.path.exists(self.errorfile):
            return read_file(self.errorfile)
        return ["%s does not exist.\n" % self.errorfile]

    def action_cancel(self):
        """Cancel a job if there is a jobid
        """
        if self.jobid:
            capture = self.capture(["scancel", self.jobid])
            return capture.output
