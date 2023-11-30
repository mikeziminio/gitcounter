/FROM rabbitmq:3.12.9-alpine
ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH

# TODO: в Dockerfile оставить установку envsubst
# Вынести в CMD - генерацию conf файла

# Генерация rabbitmq.conf с использованием переменных из .env
RUN bash $PROJECT_PATH/setup/rabbitmq/setup.sh

# Копирование файла конфигурации
COMMAND \
    bash $PROJECT_PATH/setup/rabbitmq/up.sh
    cp $PROJECT_PATH/setup/rabbitmq/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
    exec ...
