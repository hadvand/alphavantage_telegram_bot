from typing import Dict
from alpha_vantage.timeseries import TimeSeries
import requests
import matplotlib.pyplot as plt
import os


def _getter(url: str, headers: Dict, params: Dict):
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params
    )

    if response.ok:
        return response

    return response.status_code


def _get_graph(symbol: str, interval: str):
    ts = TimeSeries(key=os.environ['AV_KEY'], output_format='pandas')

    if interval == '8hrs':
        data, meta_data = ts.get_intraday(symbol=symbol, interval='5min')
    elif interval == '32hrs':
        data, meta_data = ts.get_intraday(symbol=symbol, interval='15min')
    elif interval == '3days':
        data, meta_data = ts.get_intraday(symbol=symbol, interval='30min')
    elif interval == '10days':
        data, meta_data = ts.get_intraday(symbol=symbol, interval='60min')

    data['4. close'].plot()
    file_name = symbol + interval + '.png'
    plt.savefig(file_name)

    return file_name


class SiteApiInterface:
    @staticmethod
    def getter():
        return _getter

    @staticmethod
    def get_graph():
        return _get_graph
