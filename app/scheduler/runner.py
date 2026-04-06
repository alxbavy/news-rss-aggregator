import logging
import time

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import SessionLocal
from app.integrations.rss_parser import RSSParser
from app.integrations.telegram_notifier import TelegramNotifier
from app.services.feed_polling import FeedPollingService

setup_logging()
logger = logging.getLogger()


def run_scheduler() -> None:
    logger.info(
        "Scheduler started with poll interval: %s seconds",
        settings.poll_interval_seconds,
    )

    while True:
        session = SessionLocal()
        try:
            parser = RSSParser()
            storage = None
            notifier = TelegramNotifier(
                bot_token=settings.telegram_bot_token.get_secret_value(),
            )

            service = FeedPollingService(
                parser=parser,
                storage=storage,
                notifier=notifier,
            )

            service.check_new_posts()
        except Exception:
            logger.exception("Polling cycle failed")
        finally:
            session.close()

        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    run_scheduler()
