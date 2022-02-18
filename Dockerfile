# syntax=docker/dockerfile:1
FROM ubuntu:20.04
WORKDIR /code_search

RUN apt-get update && apt-get install -y \
    python3-pip git vim
RUN pip install git+https://login:token@github.com/HSE-JetBrains-department/preprocess@master
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y golang
COPY . .
RUN rm -rf Dockerfile
RUN pip install -e .
