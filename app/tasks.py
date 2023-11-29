import asyncio
from typing import Callable
from celery import Celery
from celery.schedules import crontab
from gitanalyzer import GitAnalyzer

app = Celery("tasks", broker="amqp://gitcounter:Git_Counter_8228@localhost:5672/gitcounter")
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
