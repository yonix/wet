#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from StringIO import StringIO


class Weather():
    def __init__(self):
        self._load_settings()

    def _load_settings(self):
        import settings
        self._city_info = settings.city_info
        self._city_symbols = settings.city_symbols

    def weather(self, city_symbol):
        self.city_symbol = city_symbol
        city = self._city_symbols[self.city_symbol]
        self.city_woeid = self._city_info[city]['woeid']
        self.city_name = self._city_info[city]['name']
        self.fetch_weather()
        self.view()

    def get_woeid(self):
        return self.city_woeid

    def get_name(self):
        return self.city_name

    def fetch_weather(self):
        url = 'http://query.yahooapis.com/v1/public/yql'
        params = dict(
            q='select item from weather.forecast where woeid="{0}" \
            and u="c"'.format(self.get_woeid()),
            u="c",
            format="json",
        )

        r = requests.get(url=url, params=params)
        io = StringIO(r.content)
        self.data = json.load(io)

    def json(self):
        return self.data

    def view(self):
        c = u"\u00b0"
        a = u"\u21c6"

        print u"\n*** Weather forecast: {0} ***\n".format(self.get_name())

        condition = self.data['query']['results']['channel']['item']['condition']
        print condition['date']
        print condition['text'] + ": " + condition['temp'] + c

        forecast = self.data['query']['results']['channel']['item']['forecast']
        for i in forecast:
            print u"\n{0}, {1}".format(
                i['day'],
                i['date']
            )
            print u"{0}: {1}{2} {3} {4}{5}".format(
                i['text'],
                i['high'],
                c,
                a,
                i['low'],
                c,
            )
        print ""


if __name__ == "__main__":
    import sys
    w = Weather()
    w.weather(sys.argv[1])
