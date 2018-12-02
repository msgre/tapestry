FROM python:3.7

RUN mkdir -p /app
WORKDIR /app
ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN apt-get update && \
    apt-get -y install sshpass && \
    rm -rf /var/lib/apt/lists/*

RUN pip install ansible==2.7.2
