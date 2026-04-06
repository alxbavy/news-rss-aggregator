import logging
import time

from app.core.config import settings
from app.core.logging import setup_logging


setup_logging()
logger = logging.getLogger()


def run_scheduler() -> None:
    logger.info(
        "Scheduler started with poll interval: %s seconds",
        settings.poll_interval_seconds,
    )

    while True:
        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    run_scheduler()
