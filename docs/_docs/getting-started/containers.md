---
title: Containers
category: Getting Started
permalink: /getting-started/containers/index.html
order: 7
---

It's very likely that you might want to use qme in a headless environment
where you don't have the ability to install a ton of custom dependencies.
This is the ideal use case for containers! We will walk through the basic
build and usage for the automated Docker build here, and then how
to pull the container down to Singularity for cluster usage.

## Docker

If you want to build the container on your own, you can do that as follows:

```bash
$ git clone git@github.com:vsoch/qme
cd qme
$ docker build -t quay.io/vanessa/qme .
```

Note that you can also just pull the container - there is an automated build
for it at Quay.io at [quay.io/vanessa/qme](https://quay.io/repository/vanessa/qme?tab=tags).

```bash
$ docker pull quay.io/vanessa/qme
```

You can then test qme via shelling into the container, and exposing a port.
Commands in the container will be parsed.

```bash
$ docker run -it --entrypoint /bin/bash --rm -p 5000:5000 quay.io/vanessa/qme 
```

Also remember that you should generate and include a secret key for your container
if you want to use the interface.

```bash
$ docker run -it --entrypoint /bin/bash --env QME_SERVER_KEY=mysecretkey --rm -p 5000:5000 quay.io/vanessa/qme 
```

Then you can run a few commands:

```bash
$ qme run whoami
$ qme run ls
```

And view them in the terminal, either with get or ls:

```bash
$ qme get
Database: sqlite
{
    "executor": "shell",
    "uid": "shell-c2194940-1150-44fe-98d4-7852bcc4fa8f",
    "data": {
        "pwd": "/tmp/repo",
        "user": "root",
        "timestamp": "2020-05-21 19:43:40.330947",
        "output": [
            "root\n"
        ],
        "error": [],
        "returncode": 0,
        "pid": 9,
        "cmd": [
            "whoami"
        ],
        "status": "complete"
    },
    "command": "whoami"
}
```
```bash
$ qme ls
Database: sqlite
1  shell-cd86b90f-5362-4130-8fd7-4be7531d36f3	ls
2  shell-c2194940-1150-44fe-98d4-7852bcc4fa8f	whoami
```

And to open the dashboard, run qme start:

```bash
$ qme start
```

You should then be able to navigate to [http://0.0.0.0:5000/](http://0.0.0.0:5000/)
to see the [dashboard](../dashboard/) interface. As an example use case for a
Docker container, if you have a container with some tool inside that you want
to expose a dashboard for, you can install qme, and then have the entrypoint
be the dashboard. In a Dockerfile that might look like:

```
ENTRYPOINT ["/opt/conda/bin/qme"]
CMD ["start"]
```

But you can run it with the base qme container too! The entrypoit is already qme,
so you can just add the start argument, and run it in detached mode:

```bash
$ docker run -d --rm -p 5000:5000 quay.io/vanessa/qme start
```

Here we see the running container:

```bash
$ docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                    NAMES
478d6d9bf16c        quay.io/vanessa/qme   "/opt/conda/bin/qme …"   2 seconds ago       Up 1 second         0.0.0.0:5000->5000/tcp   mystifying_poincare
```

And we can execute a command to it, prefixed with qme run of course:

```bash
$ docker exec mystifying_poincare qme run ls /tmp
Database: sqlite
[shell-8bea6043-774f-46b2-969a-89a9b1e1728a][returncode: 0]
```

and the task will appear in our interface again at [http://0.0.0.0:5000/](http://0.0.0.0:5000/)!
So if you have some particular scientific software that you want to run in a container,
and you want to keep a record of your commands, this is a good option.
However if you want seamless interaction with your own host, Singularity is recommended, discussed next.

## Singularity

If you are working on a cluster environment (or otherwise don't want to install
dependencies) you can pull the docker container as a Singularity container.
By default it will use a sqlite database to provide a nice balance between
what you have (the ability to save a .db file in $HOME and not need a
 more robust relational database). Let's first pull the container from
quay.io:

```bash
$ singularity pull docker://quay.io/vanessa/qme
```

Access to the QueueMe executable is available when you run the container!

```bash
./qme_latest.sif ls
```

See the [Singularity tutorial]({{ site.baseurl }}/tutorials/singularity/) for more details.

