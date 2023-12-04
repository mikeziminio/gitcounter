#!/bin/bash

while ! nc -zv "$1" "$2"; do
    sleep 2
    echo "Waiting for socket $1:$2 availability..."
done

echo "Socket $1:$2 is available"
