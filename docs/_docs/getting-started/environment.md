---
title: Environment
category: Getting Started
permalink: /getting-started/environment/index.html
order: 3
---

The following environment variables can be set to determine runtime behavior.

### QME_WORKERS
the number of multiprocessing workers to use (for executors that can use it). Set to be 2*2nproc + 1 if not set.

### QME_SHELL
the default shell for an interactive manager (defaults to ipython, then checks python, and bpython)

### QME_DATABASE

the database to use. For example, you can specify just `filesystem` or `sqlite`, or `postgres` or `mysql`.
For the last three, you can optionally specify `QME_DATABASE_STRING` to include a particular
set of credentials needed for access. This will be saved in your `QME_HOME` secrets.

### QME_DATABASE_STRING

If you have a custom string for a database or file, you can specify it with `QME_DATABASE_STRING`.
(todo add expfactory examples here)
See [database setup](#database-setup) for more details.

### QME_HOME

The "home" directory for QueueMe is by default placed in your $HOME in a directory called .qme.
Within that directory, you will see the following structure:

```bash
.qme/
  config.json (- configuration
  database/   (- database for filesystem, if applicable
```

If you want to change this location, then you'll need to (more permanently) export
`QME_HOME` in your bash profile, or perhaps in a container install.

### QME_SOCKET_UPDATE_SECONDS

If you are using the dashboard (which uses web sockets) this is the number of
seconds to update it. This basically will update the dashboard table
with the content of your Qme Database.

You might next want to browse [commands]({{ site.baseurl }}/getting-started/commands/) that can
be run with qme.
