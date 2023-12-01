FROM rabbitmq:3.12.9-alpine

ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH

# Генерация rabbitmq.conf с использованием переменных из .env
RUN bash "$PROJECT_PATH/setup/rabbitmq/setup.sh"

# При запуске докера - генерация файла конфигурации и копирование его в папку /etc/
COMMAND \
    bash "$PROJECT_PATH/setup/rabbitmq/up.sh" && \
    exec rabbitmq-server
