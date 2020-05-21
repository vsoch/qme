#!/usr/bin/env python
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import sys
import pytest


def test_executor_slurm(tmp_path):
    """Test the shell executor. A shell executor should have added a returncode,
       output, and error to it's data export.
    """
    # We can't emulate slurm, so just test general executor
    from qme.main.executor import get_named_executor

    executor = get_named_executor("slurm")
    assert executor.name == "slurm"
    actions = executor.get_actions()
    for key in ["status", "output", "error", "cancel"]:
        assert key in actions

    # Task.export includes the executor specific data
    data = executor.export()
    for key in ["cmd", "pwd", "output", "error", "returncode"]:
        assert key in data
