#!/usr/bin/env python

import urllib
import os
import sys

def download(url):
    web_file = urllib.urlopen(url)
    file = open(url.split('/')[-1], 'w')
    file.write(web_file.read())
    web_file.close()
    file.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            download(sys.argv[1])
        except IOError:
            print('Filename not found.')
    else:
        print('usage: %s http://server.com/path/to/filename' % os.path.basename(sys.argv[0]))
