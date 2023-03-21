# OneBudget API

## Description

This is the OneBudget API, The goal is to make this the backend for an Open Source budgeting app.

## Getting Started

### Using Docker

1. Clone the repository
2. Start the docker containers

    ```bash
    docker-compose up --build
    ```

### Not Using Docker

1. Clone the repository
2. Generate a pair of RSA keys

    ```bash
    ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f ./privatekey
    RUN openssl rsa -in /root/.ssh/privatekey -pubout -outform PEM -out ./publickey
    ```

3. create SQLite DB at the root of the repo
