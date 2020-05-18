# QMe

[![PyPI version](https://badge.fury.io/py/qme.svg)](https://badge.fury.io/py/qme)

![docs/assets/img/logo/logo-small.png](docs/assets/img/logo/logo-small.png)

"Queue-me" is a jobs queue and dashboard generation tool that can be used
to specify executors (entities that run jobs) and actions for them. You can
use qme only on the command line, or if desired, via an interactive web dashboard.
The dashboard (and it's dependencies) are not required for using the base library.

You can run a task on the command line with `qme run` and then execute other `qme`
commands to manage or inspect it, or start a web interface that will update
automatically:

![docs/_docs/getting-started/img/dashboard/prototype.png](docs/_docs/getting-started/img/dashboard/prototype.png)

and expose executor-specific views for your tasks!

![docs/_docs/getting-started/img/executors/shell.png](docs/_docs/getting-started/img/executors/shell.png)

**under development**

## Documentation

For current documentation, see [https://vsoch.github.io/qme](https://vsoch.github.io/qme)

## License

 * Free software: MPL 2.0 License

## TODO

 - add confirm prompt to delete task in interface
 - add time stamp to metadata
 - filesystem task that exists should also be loaded
 - init (when we create config) should generate value for secret?
 - add config command to refresh secret
 - each executor should have unique id that is used for logger, database, etc.
 - design models for filesystem or relational database
 - base should be able to use a user defined database for jobs (define on onset)
