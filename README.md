# QMe

"Queue-me" is a jobs queue and dashboard generation tool that can be used
to specify executors (entities that run jobs) and actions for them.

[![PyPI version](https://badge.fury.io/py/qme.svg)](https://badge.fury.io/py/qme)

**under development**

## Documentation

This documentation will be moved to a docs folder, likely after a logo and branding
is developed, or @vsoch gets tired of writing things here!

## Install

(template in docs)

## Configuration

Configuration is optional, and will (if desired) allow you to define a custom
database for your install. When you first install qme and run it, if you haven't
configured anything, a .qme file will be created in your home, and metadata
files stored here. For many settings, you can either set or update them via
the command line client with `qme config`, or set environment variables 
at runtime (or in your bash profile) for one off changes to default configurations.

### Environment

The following environment variables can be set to determine runtime behavior.

#### QME_WORKERS
the number of multiprocessing workers to use (for executors that can use it). Set to be 2*2nproc + 1 if not set.

#### QME_SHELL

the default shell for an interactive manager (defaults to ipython, then checks python, and bpython)

#### QME_DATABASE

the database to use. For example, you can specify just `filesystem` or `sqlite`, or `postgres` or `mysql`.
For the last three, you can optionally specify `QME_DATABASE_STRING` to include a particular
set of credentials needed for access. This will be saved in your `QME_HOME` secrets.

#### QME_DATABASE_STRING

If you have a custom string for a database or file, you can specify it with `QME_DATABASE_STRING`.
(todo add expfactory examples here)
See [database setup](#database-setup) for more details.

#### QME_HOME

The "home" directory for QueueMe is by default placed in your $HOME in a directory called .qme.
Within that directory, you will see the following structure:

```bash
.qme/
  config.json (- configuration
  database/   (- database for filesystem, if applicable
```

If you want to change this location, then you'll need to (more permanently) export
`QME_HOME` in your bash profile, or perhaps in a container install.

### Database Setup

When you first run a command, without any setup a filesystem database is used, and
the metadata and files are stored in your $HOME in a hidden `.qme` directory. 
The folder with database files would be at `$HOME/.qme/database`. This
is referred to as the "filesystem" database, and is appropriate for running in headless
environments where you don't have special privileges. However, if you 
have access to a more robust database (or want to use sqlite) you have several
database options to choose from. For any of these options, you will need
to install sqlachemy, which can be done with:

```bash
pip install qme[database]
```

While the filesystem database is suitable for use cases with few tasks or just
for testing, for anything else we recommend at least using an Sqlite database
that can better be queried.

**instructions will be written for customizing database, development being done with filesystem**

### Running Commands

These sections will be expanded as the library is developed.

#### Run
You can currently run a basic terminal command (one that is executed and has error,
output, and a return code) like the following:

```bash
$ qme run ls $PWD
DATABASE: filesystem
[shell-5b8a154e-5178-4b1c-811c-d493d4349f1f][returncode: 0]
```

The command is so quick that it gives you the result immediately. In the above,
we see the executor (shell) along with the unique id (the following uuid), 
and the full command (to list the expanded $PWD) and the return code 0.

#### Get 

Once we know a task id (`shell-5b8a154e-5178-4b1c-811c-d493d4349f1f` for the above)
we likely want to get a summary of it. We can do that with `qme get`, which 
expects a task id.

```bash
$ qme get shell-452e61bd-ee9a-4a0c-8e85-f35f2b4b54a5
DATABASE: filesystem
{
    "executor": "shell",
    "uid": "shell-452e61bd-ee9a-4a0c-8e85-f35f2b4b54a5",
    "data": {
        "output": [
            "config.py\n",
            "get.py\n",
            "__init__.py\n",
            "listing.py\n",
            "__pycache__\n",
            "run.py\n"
        ],
        "error": [],
        "returncode": 0
    }
}
```

#### List

For the command line, you can easily list tasks. For the filesystem database,
since we would need to read in several json files, the listing just shows the
task ids. If you do a general list with `qme ls`, it will show all task ids:

```bash
$ qme ls
DATABASE: filesystem
1  shell-7a2f5e23-27ef-49eb-a6a6-896ddc690117
2  shell-84f90411-a53e-4d40-92b0-706e5ddfa3b9
3  shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a
4  shell-542e11ef-a1d1-47ce-90a7-40fc7829d29f
5  shell-0f85a77f-f442-46b1-88b1-7d55303b2119
6  shell-5a9e4413-b25d-4dca-826f-f9f8b27abf50
7  shell-2e65e814-388d-4617-bf89-ef307ba6fa40
8  shell-c07e9279-eee7-4778-9212-4ac617a6082e
9  shell-bcaae4db-2970-4674-9800-376c891c1454
10 shell-38307314-9825-435b-8fb6-6d37b3427a7b
11 shell-ad239488-2a27-47b9-8225-da227625e913
```

The above tasks are for the shell executor, which is the default if no special
executor is selected. You could explicitly state this like:

```bash
$ qme ls shell
DATABASE: filesystem
1  shell-7a2f5e23-27ef-49eb-a6a6-896ddc690117
2  shell-84f90411-a53e-4d40-92b0-706e5ddfa3b9
3  shell-5c61ce2b-988e-44fa-8678-a9704ca11b1a
4  shell-542e11ef-a1d1-47ce-90a7-40fc7829d29f
5  shell-0f85a77f-f442-46b1-88b1-7d55303b2119
6  shell-5a9e4413-b25d-4dca-826f-f9f8b27abf50
7  shell-2e65e814-388d-4617-bf89-ef307ba6fa40
8  shell-c07e9279-eee7-4778-9212-4ac617a6082e
9  shell-bcaae4db-2970-4674-9800-376c891c1454
10 shell-38307314-9825-435b-8fb6-6d37b3427a7b
11 shell-ad239488-2a27-47b9-8225-da227625e913
```


This library is heavily under development, not all code is in verison control,
and nowhere near ready for use!

### Environment

 * Free software: MPL 2.0 License

## TODO

 - each executor should have unique id that is used for logger, database, etc.
 - design models for filesystem or relational database
 - create GitHub workflows for tests and black formatting.
 - init should create structures in home, akin to sregistry (but with config file?)
 - base should be able to use a user defined database for jobs (define on onset)
 - client should work like a wrapped (e.g., qme run `command`)
 - basic interface should be command line, extra interface should not be required.
