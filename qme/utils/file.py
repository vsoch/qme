"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import fnmatch
import glob
import json
import os
import pickle
import tempfile


def get_latest_modified(base, pattern="*.json"):
    """Given a folder, get the latest modified file
    """
    files = recursive_find(base, pattern)
    return max(files, key=os.path.getctime)


def recursive_find(base, pattern="*.py"):
    """recursive find will yield python files in all directory levels
       below a base path.

       Arguments:
         - base (str) : the base directory to search
         - pattern: a pattern to match, defaults to *.py
    """
    for root, _, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def read_file(filename, readlines=True):
    """write_file will open a file, "filename" and write content
       and properly close the file.

       Arguments:
         - filename (str) : the filename to read
         - readlines (bool) : read lines of the file (vs all raw)
    """
    with open(filename, "r") as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def write_json(json_obj, filename, pretty=True):
    """write_json will write a json object to file, pretty printed

       Arguents:
        - json_obj (dict) : the dict to print to json
        - filename (str) : the output file to write to
    """
    with open(filename, "w") as filey:
        if pretty:
            filey.writelines(json.dumps(json_obj, indent=4, separators=(",", ": ")))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def read_json(input_file):
    """Read json from an input file.

       Arguments:
         - input_file (str) : the filename to read
    """
    with open(input_file, "r") as filey:
        data = json.loads(filey.read())
    return data


def save_pickle(obj, filename):
    """Save a pickle to file

       Arguments:
         - obj (any) : the object to pickle
        - filename (str) : the output file to write to
    """
    with open(filename, "wb") as fd:
        pickle.dump(json_obj, fd)
    return filename


def get_userhome():
    """get the user home based on the effective uid. If import of pwd fails
       (not supported for Windows) then fall back to environment variable.
    """
    try:
        import pwd

        return pwd.getpwuid(os.getuid())[5]
    except:
        return os.environ.get("HOME") or os.environ.get("HOMEPATH")


def get_user():
    """Get the name of the user. We first try to import pwd, but fallback to 
       extraction from the environment.
    """
    try:
        import pwd

        return pwd.getpwuid(os.getuid())[0]
    except:
        return os.environ.get("USER") or os.environ.get("USERNAME")


def mkdir_p(path):
    """mkdir_p attempts to get the same functionality as mkdir -p

       Arguments:
        - path (str) : the path to create
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            sys.exit("Error creating path %s, exiting." % path)


def get_tmpfile(prefix=""):
    """get a temporary file with an optional prefix. By default, the file
       is closed (and just a name returned).

       Arguments:
        - prefix (str) : prefix with this string
    """
    tmpdir = tempfile.gettempdir()
    prefix = os.path.join(tmpdir, os.path.basename(prefix))
    fd, tmp_file = tempfile.mkstemp(prefix=prefix)
    os.close(fd)
    return tmp_file


def get_tmpdir(prefix="", create=True):
    """get a temporary directory for an operation. If SREGISTRY_TMPDIR
       is set, return that. Otherwise, return the output of tempfile.mkdtemp

       Arguments:
        - prefix (str) : prefix with this string
        - create (bool) : create the folder (defaults to true) 
    """
    tmpdir = tempfile.gettempdir()
    prefix = prefix or "qme-temp"
    prefix = "%s.%s" % (prefix, next(tempfile._get_candidate_names()))
    tmpdir = os.path.join(tmpdir, prefix)
    if not os.path.exists(tmpdir) and create:
        os.mkdir(tmpdir)
    return tmpdir
