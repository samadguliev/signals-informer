from celery import Celery
from datetime import timedelta

app = Celery('scheduler',
             broker='redis://redis:6379/0',
             backend='redis://redis:6379/0',
             include=['scheduler.tasks'])

# Optional configuration, see the application user guide.
app.conf.timezone = 'UTC'
app.autodiscover_tasks()
app.conf.update(
    result_expires=3600,
)

app.conf.beat_schedule = {
    "update_prices": {
        "task": 'scheduler.tasks.update_prices',
        "schedule": timedelta(seconds=20),
    },
}

if __name__ == '__main__':
    app.start()