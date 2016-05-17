#!/usr/bin/python3

import requests
import httplib

def login2():

    s = requests.Session()
    s.auth = ('user', 'userPass')
    r = s.post('https://localhost:8443/login', verify=False)

    print(r.status_code)
    print(r.cookies)

    # cook = r.cookies.get_dict()

    # r = s.get("https://localhost:8080/api/ehs/tc/uni/jh3389", cookies=cook)
    # print(r.status_code)
    # print(r.headers)

def login():

    s = requests.Session()
    s.auth = ('user', 'userPass')
    r = s.post('https://localhost:8443/login', verify=False)

    print(r.status_code)
    print(r.cookies)

    # cook = r.cookies.get_dict()

    # r = s.get("https://localhost:8080/api/ehs/tc/uni/jh3389", cookies=cook)
    # print(r.status_code)
    # print(r.headers)


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
    login()


if __name__ == '__main__':
    main()

