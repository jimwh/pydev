#!/usr/bin/python

import sys
import cx_Oracle
import db_connector
#
# local
# rascal/rascal@127.0.0.1/XE
#
sql_resource = "select ID_, NAME_, BYTES_ from ACT_GE_BYTEARRAY where NAME_ like '%.xml'"

def download_xml_resource():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(sql_resource)
    for res in cursor:
        (source_id, name, blob_data) = res
        foo = name.split('/')
        filename = '_'.join((source_id, foo[-1]))
        file = open(filename, 'w')
        file.write(blob_data.read())
        file.close()


def main():
    if len(sys.argv) != 2:
        print('usage: %s <connection string>' % sys.argv[0])
        sys.exit(1)

    db_connector.DBConnector(sys.argv[1])
    download_xml_resource()
    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
