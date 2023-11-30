#!/bin/bash

# Инициализация env vars
source $dir_name/../../.env

# Передаю именно так, потому что не хочу делать export
RABBITMQ_USER=$RABBITMQ_USER \
RABBITMQ_PASSWORD=$RABBITMQ_PASSWORD \
RABBITMQ_VHOST=$RABBITMQ_VHOST \
RABBITMQ_PORT=$RABBITMQ_PORT \
envsubst < "$dir_name/rabbitmq.conf.template" > "$dir_name/rabbitmq.conf"
