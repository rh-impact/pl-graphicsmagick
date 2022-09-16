# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.6-slim-bullseye

LABEL org.opencontainers.image.authors="Jiri Stransky <jistr@redhat.com> and FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="GraphicsMagick ChRIS plugin" \
      org.opencontainers.image.description="ChRIS plugin that allows running arbitrary GraphicsMagick processing on images"

WORKDIR /usr/local/src/app

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install graphicsmagick

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["commandname", "--help"]
