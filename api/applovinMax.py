from datetime import datetime

import requests


class response_format:
    JSON = 'json'
    CSV = 'csv'


class response_sort:
    ASC = 'ASC'
    DESC = 'DESC'


class applovinMax:
    _url = 'https://r.applovin.com/maxReport'
    _start = ""
    _end = ""
    _api_key = ""
    _format = response_format.JSON
    _columns = ['day', 'impressions', 'ecpm', 'estimated_revenue']
    _filter_x = ""
    _sort_x = ""
    _limit = ""
    _offset = ""
    _report_type = "publisher"

    def __init__(self, api_key):
        self._api_key = api_key

    def _build_url(self, start, end, url=_url, res_format=_format, columns=','.join(_columns)):
        params_dict = {'api_key': self._api_key, 'start': start, 'end': end, 'format': res_format, 'columns': columns,
                       '_report_type': self._report_type}
        params = '&'.join(f'{key}={value}' for key, value in params_dict.items())

        return f'{url}?{params}'

    def today_revenue(self):
        today = datetime.today().strftime('%Y-%m-%d')
        req_url = self._build_url(start=today, end=today)
        res = requests.get(req_url, timeout=10).json()
        return res['results'][0]['estimated_revenue']


