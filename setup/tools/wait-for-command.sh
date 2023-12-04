#!/bin/bash

while ! command -v "$1"; do
    sleep 2
    echo "Waiting for command $1 availability..."
done

echo "Command $1 is available"
