from datetime import datetime, date, timedelta

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
        today = date.today().strftime('%Y-%m-%d')
        req_url = self._build_url(start=today, end=today)
        proxies = {"http": None, "https": None}
        res = requests.get(url=req_url, proxies=proxies, timeout=10)
        if res:
            return res.json()['results'][0]['estimated_revenue']
        else:
            print(res)
            return False

    def yesterday_revenue(self):
        yesterday = date.today() - timedelta(days=1)
        req_url = self._build_url(start=yesterday, end=yesterday)
        proxies = {"http": None, "https": None}
        res = requests.get(url=req_url, proxies=proxies, timeout=10)
        if res:
            return res.json()['results'][0]['estimated_revenue']
        else:
            print(res)
            return False

# def seven_days_revenue(self):
#     seven_days = date.today() - timedelta(days=7)
#     today = datetime.today().strftime('%Y-%m-%d')
#     req_url = self._build_url(start=today, end=seven_days)
#     res = requests.get(req_url, timeout=10).json()
#     return res['results'][0]['estimated_revenue']
