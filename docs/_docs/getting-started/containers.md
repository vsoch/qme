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

**under development**

## Singularity

If you are working on a cluster environment (or otherwise don't want to install
dependencies) you can pull the docker container as a Singularity container.
By default it will use a sqlite database to provide a nice balance between
what you have (the ability to save a .db file in $HOME and not need a
 more robust relational database).

