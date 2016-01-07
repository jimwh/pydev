#!/usr/bin/python

import urllib2
import httplib2 as http
import json
from urlparse import urlparse
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth


def foologin2():

    s = requests.Session()
    s.auth = ('SafetyStratus', 'IwUTRkDmD5H3j650')
    r = s.post('https://test.rascal.columbia.edu/login')

    print(r.status_code)
    print(r.cookies)

    cook = r.cookies.get_dict()

    payload = [{'uni': 'yi77'}]

    r = s.get("https://test.rascal.columbia.edu/api/ehs/tc/course/TC0509/from/2014/12/31/to/2015/03/31/",
              cookies=cook)
    print(r.status_code)
    print(r.headers)


def main():
    foologin2()


if __name__ == '__main__':
    main()

