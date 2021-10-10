FROM ubuntu:20.04

LABEL mantainer="Dimas Adrian Mukti <dadrianm25@gmail.com>"

USER root

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LIBGL_ALWAYS_INDIRECT=1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --fix-missing \
    build-essential \
    git \
    pkg-config \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN apt-get install -y \
    python3 python3-pyqt5 python3-pip python3-venv

RUN usermod -a -G audio root
RUN usermod -aG video root

WORKDIR /app

RUN python3 -m venv env

COPY requirements.txt requirements.txt
RUN env/bin/pip install -r requirements.txt

COPY . .

ENTRYPOINT ["env/bin/python", "dashboard.py"]