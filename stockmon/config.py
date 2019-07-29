"""Default settings."""

import os

from stockmonlib import API_URL


class Config:  # pylint: disable=too-few-public-methods
    API_KEY = os.environ.get('API_KEY', 'demo')
    API_URL = os.environ.get('API_URL', API_URL)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    SYMBOL = os.environ.get('SYMBOL', None)
    DAYS = os.environ.get('DAYS', None)
