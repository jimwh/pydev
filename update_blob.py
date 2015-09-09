#!/usr/bin/python

import os
import sys
import cx_Oracle

from db import db_connector
from db import jproperties


SQL_INSERT_BLOB = "insert into foobar(id, filename, content) values(:1, :2, :3)"

SQL_UPDATE_BLOB = "update foobar set content = :1 where id=1 and filename='foome'"

def insert_blob():
    binary_data = read_file()

    cursor = db_connector.DBConnector.cursor()

    binary_var = cursor.var(cx_Oracle.BLOB)
    binary_var.setvalue(0, binary_data)
    cursor.execute(SQL_INSERT_BLOB, [1, 'foome', binary_var])
    # cursor.execute(SQL_INSERT_BLOB, [1, 'foome', '/home/jh3389/Downloads', 'PastedGraphic-1.tiff'])
    db_connector.DBConnector.commit()
    cursor.close


def update_blob():
    binary_data = read_file()
    cursor = db_connector.DBConnector.cursor()
    binary_var = cursor.var(cx_Oracle.BLOB)
    binary_var.setvalue(0, binary_data)
    cursor.execute(SQL_UPDATE_BLOB, [binary_var])
    db_connector.DBConnector.commit()
    cursor.close


def read_file():
    # file = open('/home/jh3389/Downloads/PastedGraphic-1.tiff', 'rb')
    file = open('/home/jh3389/Downloads/tjc2155_certificate.pdf', 'rb')
    data = file.read()
    file.close()
    return data

def dump_to_file(file_name, blob_data):
    try:
        file = open(file_name, 'w')
        file.write(blob_data.read())
        file.close()
    except IOError:
        print('i/o error... {}'.format(file_name))

def download_blob():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute('select content from foobar where id=1')
    res = cursor.fetchone()

    if res is not None:
        file_name = 'foome.pdf'
        try:
            file = open(file_name, 'w')
            file.write(res[0].read())
            file.close()
        except IOError:
            print('i/o error... {}'.format(file_name))

    cursor.close

def main():
    prop = jproperties.Properties()
    prop.load("./db/db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        return 1
    db_connector.DBConnector(connection_str)

    ### insert_blob()
    update_blob()
    download_blob()

    db_connector.DBConnector.close()

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())

