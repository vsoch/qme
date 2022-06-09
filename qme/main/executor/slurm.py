"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import os
import re

from qme.exceptions import OutputParsingError
from qme.utils.file import read_file
from .shell import ShellExecutor

bot = logging.getLogger("qme.main.executor.slurm")


class SlurmExecutor(ShellExecutor):
    """A slurm executor parses an srun command and exposes options for getting
    a job status.
    """

    name = "slurm"
    matchstring = "^sbatch"

    def __init__(self, taskid=None, command=None):
        super().__init__(taskid, command)
        self.actions = {
            "status": self.action_get_status,
            "output": self.action_get_output,
            "error": self.action_get_error,
            "cancel": self.action_cancel,
        }

    def execute(self, cmd=None, message=None):
        """Execute a system command and return output and error. Execute
        should take a cmd (a string or list) and execute it according to
        the executor. Attributes should be set on the class that are
        added to self.export. Since the functions here are likely needed
        by most executors, we create a self._execute() class that is called
        instead, and can be used by the other executors.
        """
        self.message = message
        self._execute(cmd)
        if self.data["returncode"] == 0:

            # Find the job id, and any --out or --error files
            match = re.search("[0-9]+", self.data["output"][0])
            if not match:
                raise OutputParsingError(
                    f"Unable to derive job id from {self.data['output']}"
                )
            self.data["jobid"] = match.group()

            # Get output file, or default to $PWD/slurm-<jobid>
            self.data["errorfile"] = os.path.join(
                self.pwd, "slurm-%s.err" % self.data["jobid"]
            )
            self.data["outputfile"] = os.path.join(
                self.pwd, "slurm-%s.out" % self.data["jobid"]
            )

            match = re.search(r"(--out|-o) (?P<output>[^\s-]+)", self.command)
            if match:
                self.data["outputfile"] = match.groups("output")[1]

            match = re.search(r"(--err|-e) (?P<error>[^\s-]+)", self.command)
            if match:
                self.data["errorfile"] = match.groups("error")[1]

    # Actions

    def action_get_status(self, data):
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
        jobid = data.get("jobid")
        if jobid:
            capture = self.capture(
                ["sacct", "--job", jobid, "--format=%s" % fmt, "--noheader"]
            )
            values = {}
            output = [x for x in capture.output[0].strip().split(" ") if x]
            for i, varname in enumerate(fmt.split(",")):
                values[varname] = output[i]
            return values

    def action_get_output(self, data):
        """Get error stream, if the file exists."""
        outputfile = data.get("outputfile")
        if os.path.exists(outputfile):
            return read_file(outputfile)
        return ["%s does not exist.\n" % outputfile]

    def action_get_error(self, data):
        """Get just output stream, if the file exists."""
        errorfile = data.get("outputfile")
        if os.path.exists(errorfile):
            return read_file(errorfile)
        return ["%s does not exist.\n" % errorfile]

    def action_cancel(self, data):
        """Cancel a job if there is a jobid"""
        jobid = data.get("jobid")
        if jobid:
            capture = self.capture(["scancel", jobid])
            return capture.output
