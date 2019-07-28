"""Stock monitoring library."""
import abc
import logging
from json import JSONDecodeError

import requests

API_URL = 'https://www.alphavantage.co/query'


class Stock:
    """Provide an interface to gathering stick information."""

    FUNCTION = None
    __metaclass__ = abc.ABCMeta

    def __init__(self, symbol, api_key='demo', api_url=API_URL, output='compact'):
        """
        Create a stock object based the given symbol.

        Args:
            symbol: Unique short hand descriptor for a company's stock
            api_key: The API key for the Alpha Advantage stock application
            api_url: The base API URL
            output: Output length either compact or full

        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self.symbol = symbol
        self.api_key = api_key
        self.api_url = api_url
        self.output = output
        self._headers = {'ContentType': 'application/json'}
        self._data = None
        self.__params = None

    @property
    @abc.abstractmethod
    def series(self):
        return

    @property
    def meta_data(self):
        return Metadata(self.data.get('Meta Data', {}))

    @property
    def _params(self):
        if self.__params is None:
            self.__params = {
                'apikey': self.api_key,
                'function': self.FUNCTION,
                'symbol': self.symbol,
                'outputsize': self.output
            }
        return self.__params

    @_params.setter
    def _params(self, value):
        self.__params = value

    @property
    def data(self):
        if self._data is None:
            self._logger.debug('Fetching data from: %s', self.api_url)
            with requests.Session() as session:
                try:
                    response = session.get(url=self.api_url,
                                           params=self._params,
                                           headers=self._headers)
                    response.raise_for_status()
                    data = response.json()
                except JSONDecodeError:
                    self._logger.exception('Failed to parse JSON object')
                error_message = data.get('Error Message')
                if error_message:
                    raise RuntimeError(f'API call returned an error: {error_message}')
                self._data = data
        return self._data

    def __repr__(self):
        """
        String representation of class.

        Returns: string

        """
        return self.__str__()

    def __str__(self):
        """
        String representation of class.

        Returns: string

        """
        return f'{self.__class__.__name__}({self.meta_data})'


class StockDailyAdjusted(Stock):
    FUNCTION = 'TIME_SERIES_DAILY_ADJUSTED'

    def __init__(self, symbol, api_key='demo', api_url=API_URL, output='compact'):
        """
        Provide an interface for the Daily Adjusted type of stock data.

        Args:
            symbol: Unique short hand descriptor for a company's stock
            api_key: The API key for the Alpha Advantage stock application
            api_url: The base API URL
            output: Output length either compact or full

        """
        super().__init__(symbol=symbol, api_key=api_key, api_url=api_url, output=output)
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def series(self):
        return (TimeSeriesDaily({k: v}) for k, v in
                self.data.get('Time Series (Daily)', {}).items())


class Metadata:

    def __init__(self, data):
        """
        Provide a structured object for Metadata.

        Args:
            data: metadata from the API

        """
        self._data = data

    @property
    def information(self):
        return self._data.get('1. Information')

    @property
    def symbol(self):
        return self._data.get('2. Symbol')

    @property
    def refreshed(self):
        return self._data.get('3. Last Refreshed')

    @property
    def output_size(self):
        return self._data.get('4. Output Size')

    @property
    def tz(self):
        return self._data.get('Time Zone')

    def __repr__(self):
        """
        String representation of class.

        Returns: string

        """
        return self.__str__()

    def __str__(self):
        """
        String representation of class.

        Returns: string

        """
        return f'{self.symbol}@{self.refreshed}'


class TimeSeries:
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        """
        Provide a structured object for Time Series data.

        Args:
            data: data from the api to parse

        """
        self._data = data

    @property
    def date(self):
        return list(self._data.keys()).pop()

    @property
    def open(self):
        return self._data[self.date].get('1. open')

    @property
    def high(self):
        return self._data[self.date].get('2. high')

    @property
    def low(self):
        return self._data[self.date].get('3. low')

    @property
    def close(self):
        return self._data[self.date].get('4. close')

    @property
    def adjusted_close(self):
        return self._data[self.date].get('5. adjusted close')

    @property
    def volume(self):
        return self._data[self.date].get('6. volume')

    @property
    def dividend(self):
        return self._data[self.date].get('7. dividend amount')

    @property
    def split_coefficient(self):
        return self._data[self.date].get('8. split coefficient')


class TimeSeriesDaily(TimeSeries):
    """Provide a structured object for Daily Time Series data."""


def main():
    logging.basicConfig(level=logging.DEBUG)
    stock = StockDailyAdjusted(symbol='MSFT')
    print(stock.meta_data)


if __name__ == '__main__':
    main()
