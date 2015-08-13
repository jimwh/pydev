#!/usr/bin/env python

import urllib
import sys

def download(url):
    url_file = urllib.urlopen(url)
    file = open(url.split('/')[-1], 'w')
    file.write(url_file.read())
    url_file.close()
    file.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            download(sys.argv[1])
        except IOError:
            print('Filename not found.')
    else:
        print('usage: %s http://server.com/path/to/filename' % sys.argv[0])
