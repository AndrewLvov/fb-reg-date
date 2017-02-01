#!/usr/bin/env python

from dateutil.parser import parse as date_parse
import csv
import requests
from urllib.parse import urlencode
from datetime import date, datetime, timedelta


def print_dates():
    for fbid, username, record_date in gather_registration_dates():
        if record_date is None:
            record_date_formatted = '*unknown*'
        else:
            record_date_formatted = record_date.isoformat()

        print(','.join([username,
                        fbid,
                        record_date_formatted]))


def find_registration_date(token):
    """
    Find registration date of a user in Facebook
    :param token: user client token which allows his feed access
    :return:
    """
    api_server = 'https://graph.facebook.com'
    step = timedelta(days=90)
    start_time = date(2004, 2, 4)

    while start_time < datetime.now().date():
        start_time += step
        path = "/v2.8/me/feed"

        params = {
            'access_token': token,
            'fields': ','.join(['created_time']),
            'until': start_time.isoformat()
        }
        url = "{server}{path}?{params}".format(
            server=api_server, path=path, params=urlencode(params))

        response = requests.get(url)
        records = response.json()['data']
        # last record is birthday event. So take the one before that
        # the first user record should point to date of registration
        # we rely on the fact that response from FB is sorted by time
        if len(records) > 1:
            first_record = records[-2]['created_time']
            return date_parse(first_record).date()
            # found oldest record, no need to continue for this user


def gather_registration_dates():
    with open('data/users.csv') as f:
        reader = csv.reader(f)
        for fbid, token, username in reader:
            yield fbid, username, find_registration_date(token)


if __name__ == '__main__':
    print_dates()
