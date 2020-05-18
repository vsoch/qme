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
pip install qme[database]
```

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

We will be added documentation for sqlite, postgres, and mysql databases (and customizing
them) when they are implemented.

If you want some help with your configuration, please don't be afraid to [reach out](https://github.com/{{ site.repo }}/issues). You might next want to see how [environment variables]({{ site.baseurl }}/getting-started/environment/) can further customize your usage of qme.
