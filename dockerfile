
FROM ubuntu:latest

# Avoid warnings by switching to noninteractive
ARG DEBIAN_FRONTEND=noninteractive

ENV DOCKERCONTAINER=true
# update/upgrade APIT
RUN apt update && apt upgrade -y
# install dependencies
RUN apt install -y software-properties-common \
    build-essential \
    curl \
    libpq5 \
    libpq-dev \
    openssh-client
# add repository for python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa
# update APT library
RUN apt update
# install python 3.11
RUN apt install -y python3.11 \
    python3.11-distutils \
    python3.11-venv\
    python3.11-dev

# install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

RUN python3.11 -m venv venv
# Enable venv
ENV PATH="./venv/bin:$PATH"

# Install dependencies.
ADD requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -U pip wheel -r /app/requirements.txt

# Add application code.
COPY . /api/

RUN mkdir /root/.ssh

#RUN chmod 600 /root/.ssh

# Generates RSA keys
RUN ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f /root/.ssh/privatekey
RUN openssl rsa -in /root/.ssh/privatekey -pubout -outform PEM -out /root/.ssh/publickey

#RUN chmod 600 /root/.ssh/

# Renames public key
#RUN mv /root/.ssh/privatekey.pub /root/.ssh/publickey

# Start server using uvicorn
CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT