"""Default settings."""

import os

from stockmonlib import API_URL


class Config:
    API_KEY = os.environ.get('API_KEY', 'demo')
    API_URL = os.environ.get('API_URL', API_URL)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
