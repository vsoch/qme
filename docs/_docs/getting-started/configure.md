---
title: Configuration
category: Getting Started
permalink: /getting-started/configure/index.html
order: 2
---

Configuration is optional, and will (if desired) allow you to define a custom
database for your install. For many settings, you can either set or update them via
the command line client with `qme config`, or set [environment variables](../environment/) 
at runtime (or in your bash profile) for one off changes to default configurations.
When you first install qme and run it, if you haven't configured anything, 
a .qme folder will be created in your home, and metadata files stored here:

```bash
$ tree $HOME/.qme
/home/vanessa/.qme
└── config.ini
```

We call this the [environment variable](../environment/) `QME_HOME`.

## Databases

QueueMe uses some backend database to keep track of your tasks.
While the filesystem database (default) is suitable for use cases with few tasks or just
for testing, for anything else we recommend at least using an Sqlite database
that can better be queried. As a reminder, to [install]({{ site.baseurl }}/install/)
the sqlalchemy dependencies for this, you need to do:

```bash
$ pip install qme[database]
```

and then to set the database to be sqlite, just run:

```bash
$ qme config --database sqlite
```

Using some kind of relational database, or at least sqlite, will give
you a much more rich listing of your tasks because we don't need to stress
the filesystem to read each one from a json file.
More details on database types are included below.


### Filesystem

The default database, the `filesystem` that doesn't require any additional dependencies,
is considered a dummy or testing database. It will, by default, generate a "database"
folder in this `QME_HOME`:

```bash
$ tree $HOME/.qme
/home/vanessa/.qme
├── config.ini
├── dashboard.log
└── database
```

Once you run an executor, a subfolder will be created based on the name of
the executor (e.g., shell) and within that folder, one json file will be created
per executor:

```bash
$ tree $HOME/.qme
/home/vanessa/.qme
├── config.ini
├── dashboard.log
└── database
    └── shell
        ├── shell-67ecf4a0-bc62-4d0e-8e45-8bf84c87ef99.json
        ├── shell-7b176033-56c9-4421-ac62-0c5c6b62d2f8.json
        ├── shell-a561702d-404e-4fb2-be27-57496b32ac46.json
        ├── shell-aee37073-b246-4384-bff0-ccec7bdefa00.json
        ├── shell-c63a1f01-7266-49cc-8d65-1b14d06a109d.json
        └── shell-d62d1dee-d21d-4e0d-9f95-75e139d9c4d2.json
```

If you've changed your database and want to update it back to be the filesystem,
just run:

```bash
$ qme config --database filesystem
```

### Sqlite

Sqlite is a reasonable choice for most use cases, as it appropriately scales enough for
the general user, and allows for relational database-like functionality without
needing anything other than permission to write a file. If you want to set a sqlite
database as default from the command line, just run:

```bash
$ qme config --database sqlite
Configuration saved with database sqlite
```

And the default sqlite database will be at a location in your QME_HOME ($HOME/.qme)
in a file `QME_DATABASE_STRING`, which defaults to `qme.db` and can be set in 
the [environment](../environment/). You can set this to be more permanent by setting
it in your config file like this:

```bash
$ qme config --database sqlite://mydatabase.db
Configuration saved with database sqlite://mydatabase.db
```

would then create `$HOME/.qme/mydatabase.db` as the default sqlite database. Again,
if you need to "one off" this setting for a particular environment or command,
you can export `QME_DATABASE` and `QME_DATABASE_STRING`:

```bash
export QME_DATABASE=sqlite
export QME_DATABASE_STRING=mydatabase.db
```

to achieve the same result.


### Postgres and MySql

Both postgres and mysql have the same format for the database string, albeit
they interact with different databases, and have different prefixes. Here is
how you can set either:

```bash
$ qme config --database mysql+pymysql://username:password@host/dbname
# or
$ qme config --database postgresql://username:password@host/dbname
```

This is **strongly** recommended to be set as an environment variable so that you don't
write credentials to a text file. So you instead might do this:

```bash
$ qme config --database mysql+pymysql
# or
$ qme config --database postgresql
```

and then export the rest via an environment variable:

```bash
export QME_DATABASE_STRING=username:password@host/dbname
```

which would work for both types.

## Executor Parameters

Each executor is allowed to define it's own parameters, and they can be
set in the configuration file with `qme config --set`. The general format is:

```bash
$ qme config --set <executor> <key> <value>
```

For example, let's say we wanted to define the sacct format string for the slurm executor.
We might do:

```bash
$ qme config --set slurm sacct_format jobid,jobname,partition,alloccpus,elapsed,state,exitcode
Configuration saved with executor.slurm sacct_format jobid,jobname,partition,alloccpus,elapsed,state,exitcode
```

And this would result in the following config file (which you could also update by hand,
if you so chose):

```
$ cat /home/vanessa/.qme/config.ini 
[DEFAULT]
database = sqlite
databaseconnect = 

[executor.shell]

[executor.slurm]
sacct_format = jobid,jobname,partition,alloccpus,elapsed,state,exitcode
```

If you want some help with your configuration, please don't be afraid to [reach out](https://github.com/{{ site.repo }}/issues). You might next want to see how [environment variables]({{ site.baseurl }}/getting-started/environment/) can further customize your usage of qme.
