#!/bin/bash

echo "Waiting for command $1 availability..."

while ! command -v "$1" &> /dev/null; do
    sleep 0.1
done
