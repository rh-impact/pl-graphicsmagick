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

GraphicsMagick can also convert between file formats simply by
specifying an output file extension different from the input file
extension.

## Installation

`pl-graphicsmagick` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl-graphicsmagick)

## Running locally

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-graphicsmagick` as a container:

```shell
singularity exec docker://fnndsc/pl-graphicsmagick chris-gm --single "args..." input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl-graphicsmagick chris-gm --help
```

## How to use the plugin

`chris-gm` can operate in:

* Single mode - a single GraphicsMagick call is made. Use `-s` or
  `--single` argument to specify the GraphicsMagick command arguments.

* Batch mode - one GraphicsMagick call is made per each file in the
  input directory. Use `-b` or `--batch` to specify the GraphicsMagick
  command arguments.

It is required to provide either `-s/--single` or `-b/--batch` but not
both at the same time.

Both single and batch command argument supports variable substitution.
These variables work with both `--single` and `--batch`:

* `%INDIR%` - resolves to the input directory.

* `%OUTDIR%` - resolves to the output directory.

Additionally, `--batch` supports variables for the file that
`chris-gm` is currently operating on in the batch loop:

* `%FILE%` - resolves to the file name being operated on. This does
  not include the input directory, so the full path in the command is
  usually specified as `%INDIR%/%FILE%`.

* `%FILEBASE%` - resolves to the base file name (without extension).
  This is useful when performing conversion to different image
  formats. E.g. you can specify input path as `%INDIR%/%FILE%` and
  output path as `%OUTDIR%/%FILEBASE%.png` to convert all input files
  to PNG format.

* `%FILEEXT%` - resolves to file extension (if any), including the
  period that separates it from the base file name. `%FILE%` can be
  alternatively written as `%FILEBASE%%FILEEXT%`.

After the single/batch command argument, two positional arguments are
required. The first is a directory containing input data, the second
is a directory where to create output data.

## Examples

```shell
mkdir incoming/ outgoing/
mv some.jpg other.jpg incoming/

# Single mode without variable substitution
singularity exec docker://fnndsc/pl-graphicsmagick:latest chris-gm --single "convert incoming/some.jpg -blur 3 outgoing/some.jpg" incoming/ outgoing/

# Single mode with variable substitution
singularity exec docker://fnndsc/pl-graphicsmagick:latest chris-gm --single "convert %INDIR%/other.jpg -resize 100x100 %OUTDIR%/other.jpg" incoming/ outgoing/

# Batch mode - will resize all images to 100x100 pixels.
# The names of the files in the output dir will be the same as in the input dir.
singularity exec docker://fnndsc/pl-graphicsmagick:latest chris-gm --batch "convert %INDIR%/%FILE% -resize 100x100 %OUTDIR%/%FILE%" incoming/ outgoing/

# Batch mode - will convert all images to PNG.
# The base names of the files in output the dir will be the same as
# in the input dir, but the extension is different.
singularity exec docker://fnndsc/pl-graphicsmagick:latest chris-gm --batch "convert %INDIR%/%FILE% %OUTDIR%/%FILEBASE%.png" incoming/ outgoing/
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
