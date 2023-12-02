#!/bin/bash

echo "Waiting for socket $1:$2 availability..."

while ! nc -zv "$1" "$2" &> /dev/null; do
    sleep 0.1
done
