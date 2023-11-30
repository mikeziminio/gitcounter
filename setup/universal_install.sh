#!/bin/bash

#
# Подходит далеко не для всех пакетов, потому что названия и способ установки пакетов может отличаться в разных
# дистрибутивах.
# Я закомментировать update, т.к. он не удобен при частых тестах.
#

if [ -f /etc/debian_version ]; then
    # Debian или его производные (Ubuntu и т.д.)
    # apt-get update
    apt-get install -y "$1"
elif [ -f /etc/alpine-release ]; then
    # Alpine Linux
    # apk update
    apk add "$1"
elif [ -f /etc/redhat-release ]; then
    # Red Hat и его производные (CentOS и т.д.)
    if command -v dnf &> /dev/null; then
        # dnf update
        dnf install -y "$1"
    elif command -v yum &> /dev/null; then
        # yum update
        yum install -y "$1"
    else
        echo "Неизвестный пакетный менеджер для Red Hat / Centos (команды yum и dnf недоступны)."
        exit 1
    fi
else
    echo "Ваш дистрибутив linux не поддерживается. " \
         "Добавьте инструкции установки пакетов в файл config/universal_installer.sh"
    exit 1
fi
