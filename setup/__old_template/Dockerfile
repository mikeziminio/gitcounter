FROM rabbitmq:3.12.9-alpine

ARG PROJECT_PATH
WORKDIR $PROJECT_PATH

COPY ./setup/universal_install.sh ./setup/universal_install.sh
COPY ./setup/rabbitmq/setup.sh ./setup/rabbitmq/setup.sh
COPY ./setup/rabbitmq/up.sh ./setup/rabbitmq/up.sh

# Генерация rabbitmq.conf с использованием переменных из .env
RUN /bin/bash ./setup/rabbitmq/setup.sh

# При запуске докера - генерация файла конфигурации и копирование его в папку /etc/
CMD [ \
    "/bin/bash", "-c", \
    "\"$PROJECT_PATH/setup/rabbitmq/up.sh\" && exec rabbitmq-server" \
]
