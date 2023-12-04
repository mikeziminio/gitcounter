import asyncio
from typing import Callable
from celery import Celery
from celery.schedules import crontab
from gitanalyzer import GitAnalyzer
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.dirname(__file__) + "/../.env")
load_dotenv(env_path)

RABBITMQ_USER = os.environ["RABBITMQ_USER"]
RABBITMQ_PASSWORD = os.environ["RABBITMQ_PASSWORD"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
RABBITMQ_CONTAINER_PORT = os.environ["RABBITMQ_CONTAINER_PORT"]
RABBITMQ_VHOST = os.environ["RABBITMQ_VHOST"]

broker_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_CONTAINER_PORT}/{RABBITMQ_VHOST}"

app = Celery("tasks", broker=broker_url)
git_analyzer = GitAnalyzer()


def async_to_sync(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        asyncio.run(func(*args, **kwargs))
    return wrapper


@app.task
@async_to_sync
async def update_all_repos_stat():
    await git_analyzer.update_all_repos_stat()


@app.on_after_configure.connect
def setup_regular_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(crontab(minute="*/5"), update_all_repos_stat.s())
