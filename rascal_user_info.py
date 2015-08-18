#!/usr/bin/python

import sys
import cx_Oracle
import db_connector
import jproperties

def main():
    prop = jproperties.Properties()
    prop.load("db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        sys.exit(1)

    db_connector.DBConnector(connection_str)

    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: %s [prod|dev|staging|local] <uni>' % sys.argv[0])
        sys.exit(1)
    main()
