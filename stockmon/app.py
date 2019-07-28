import logging
from functools import reduce

from flask import Flask

from stockmon.config import Config
from stockmonlib import StockDailyAdjusted

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=app.config.get('LOG_LEVEL'))


def get_daily_adjusted(symbol, days=None):
    stock = StockDailyAdjusted(symbol=symbol,
                               api_key=app.config.get('API_KEY'),
                               api_url=app.config.get('API_URL'))
    data = list(stock.series)[:days]
    return data


@app.route('/stockmon/v1.0/stock/<string:symbol>/close/<int:days>',
           methods=['GET'])
def stock_close(symbol, days):
    data = [day.close for day in get_daily_adjusted(symbol, days)]
    result = {
        'data': {
            'symbol': symbol,
            'series': data,
            'days': days,
            'average': reduce(lambda a, b: a + float(b), data, 0) / days
        }
    }
    return result


if __name__ == '__main__':
    app.run(debug=True)