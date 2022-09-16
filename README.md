# GraphicsMagick plugin for _ChRIS_

<!-- [![Version](https://img.shields.io/docker/v/fnndsc/pl-appname?sort=semver)](https://hub.docker.com/r/fnndsc/pl-appname) -->
[![MIT License](https://img.shields.io/github/license/rh-impact/pl-graphicsmagick)](https://github.com/rh-impact/graphicsmagick/blob/main/LICENSE)
[![ci](https://github.com/rh-impact/pl-graphicsmagick/actions/workflows/ci.yml/badge.svg)](https://github.com/rh-impact/pl-graphicsmagick/actions/workflows/ci.yml)

## Abstract

`pl-graphicsmagick` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in images as input files and
creates images processed by [GraphicsMagick](http://www.graphicsmagick.org)
as output files.

To get an idea of what GraphicsMagick is capable of, look at the list
of [GraphicsMagick
utilities](http://www.graphicsmagick.org/utilities.html).

Especially the [convert
utility](http://www.graphicsmagick.org/convert.html) is popular and
can do various operations on images: resize, blur, sharpen, crop,
dither, flip, rotate, adjust brightness-saturation-hue etc.

## Installation

`pl-graphicsmagick` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-graphicsmagick)

## Running locally

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-graphicsmagick` as a container:

```shell
singularity exec docker://fnndsc/pl-graphicsmagick chris-gm -c "args..." input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-graphicsmagick chris-gm --help
```

## Plugin parameters

`chris-gm` requires a `-c <COMMAND_ARGS>` (or `--command-args
<COMMAND_ARGS>`) argument and two positional arguments. The
`--command-args` is a string with all the arguments that you would
pass to GraphicsMagick if you were to execute `gm` command directly.
The positional arguments are a directory containing input data, and a
directory where to create output data.

The value of the `--command-args` argument can contain variables
`%INDIR%` and `%OUTDIR%` which get substituted for the input and
output directories, respectively. The variable substitution is not too
useful when using `chris-gm` on the command line, but it is useful
when executing the plugin from ChRIS, so that you can easily reference
the input/output directories from the GraphicsMagick command.

Example:

```shell
mkdir incoming/ outgoing/
mv some.jpg other.jpg incoming/

# without variable substitution
singularity exec docker://fnndsc/pl-graphicsmagick:latest chris-gm -c "convert incoming/some.jpg -blur 3 outgoing/some.jpg" incoming/ outgoing/

# with variable substitution
singularity exec docker://fnndsc/pl-graphicsmagick:latest chris-gm -c "convert %INDIR%/other.jpg -resize 100x100 %OUTDIR%/other.jpg" incoming/ outgoing/
```

## Development

To set up virtualenv for development:

```
make virtualenv-requirements
```

To run unit tests (requires GraphicsMagick installed locally):

```
make test
```

### Building

Build a local container image:

```shell
docker build -t localhost/pl-graphicsmagick .
```

### Running from locally built image

Mount the source code `app.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/app.py:/usr/local/lib/python3.10/site-packages/app.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-graphicsmagick chris-gm --help
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-graphicsmagick:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-graphicsmagick:dev pytest
```

Alternatively use the aforementioned:

```shell
make virtualenv-requirements
make test
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-graphicsmagick:1.2.3 .
docker push docker.io/fnndsc/pl-graphicsmagick:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-graphicsmagick:dev chris_plugin_info > chris_plugin_info.json
```
