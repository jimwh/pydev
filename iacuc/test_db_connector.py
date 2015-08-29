#!/usr/bin/python

from iacuc import db_connector

connector = None
def test_version():
    print(db_connector.DBConnector.version())

def main():
    db_connector.DBConnector("rascal/rascal@127.0.0.1/XE")
    test_version()

if __name__ == '__main__':
    main()

