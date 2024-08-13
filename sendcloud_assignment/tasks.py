import httpx
from celery.app import shared_task

import logging

from sendcloud_assignment import constants

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=constants.RETRY_EXCEPTIONS,
    retry_kwargs={
        "max_retries": constants.RETRY_COUNT,
        "countdown": constants.RETRY_DELAY,
    },
)
def set_timer_task(url: str) -> None:
    """Call the url.

    Retry in case it raises one of the predetermined Exceptions. On any other exception we don't retry as we don't
        know what the problem was.
    """
    response = httpx.get(url, timeout=1)
    # Log the result regardless of the response status as we want to know if the task was executed
    logger.info(f"Successfully completed task: {response=}")
    response.raise_for_status()
