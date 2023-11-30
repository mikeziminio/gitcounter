#!/bin/bash

# Получение абсолютного пути к папке текущего скрипта
dir_name=$(dirname "$(realpath "$0")")

# Установка пакета GNU gettext, который включает в себя envsubst
bash $dir_name/../universal_install.sh gettext

