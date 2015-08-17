#!/usr/bin/python

import sys
import os
import cx_Oracle
import db_connector

#
# local:  rascal/rascal@127.0.0.1/XE
#
def main():
    if len(sys.argv) != 3:
        print('usage: %s <connection string> <uni>' % sys.argv[0])
        sys.exit(1)

    db_connector.DBConnector(sys.argv[1])
    ### download_attachment(sys.argv[2])
    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
