from httpx import HTTPStatusError, TimeoutException

RETRY_COUNT = 24
RETRY_DELAY = 3600
RETRY_EXCEPTIONS = (HTTPStatusError, TimeoutException)
