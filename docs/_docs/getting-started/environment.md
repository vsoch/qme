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

the database to use. For example, you can specify just `filesystem` or `sqlite`, or `postgresql` or `mysql+pymysql` 
for mysql. For the last three, you can optionally specify `QME_DATABASE_STRING` to include a particular
set of credentials needed for access, and this is recommended over providing the values into the config,
which would save credentials in your `QME_HOME` secrets (not recommended). To export a particular
database type, here are examples:

```bash
export QME_DATABASE=mysql+pymysql
export QME_DATABASE=postgresql
export QME_DATABASE=filesystem
export QME_DATABASE=sqlite
```

For more permanent settings, you should use the [configure client](../configure/) instead.

### QME_DATABASE_STRING

If you have a custom string for a database or file, you can specify it with `QME_DATABASE_STRING`.
For example, sqlite might look like this:

```bash
export QME_DATABASE_STRING=mydatabase.db
```
and would create `mydatabase.db` in your `QME_HOME`. For a relational database with
username, password, and tables, you would export a full string:

```bash
export QME_DATABASE_STRING=username:password@host/dbname
```

See [database setup](../configure/index.html#databases) for more details.

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

### QME_LOG_LEVEL

If you want to set the logging level from the environment, set `QME_LOG_LEVEL` to 
one of "WARNING" "DEBUG" "INFO" "CRITICAL" "ERROR" or "FATAL". For example, to silence
most all messages, we might set it to fatal:

```bash
export QME_LOG_LEVEL=FATAL
```

You can override the environment default by way of using the `--log_level` flag:

```bash
$ qme --log_level INFO get
```

If you set an environment level that is not one of the choices, it will default
to using info. If you provide an inccorect value to `--log_level` you will be asked
to run the command again and choose from the valid choices.


### QME_SOCKET_UPDATE_SECONDS

If you are using the dashboard (which uses web sockets) this is the number of
seconds to update it. This basically will update the dashboard table
with the content of your Qme Database.

You might next want to browse [commands]({{ site.baseurl }}/getting-started/commands/) that can
be run with qme.
