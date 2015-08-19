#!/usr/bin/python

import sys
import cx_Oracle
import db_connector

SQL_1 = "select NAME_, BYTEARRAY_ID_ from ACT_HI_DETAIL where TASK_ID_ = :task_id"

SQL_2 = "select bytes_ from ACT_GE_BYTEARRAY where ID_= :byte_array_id"


def begin_print_var(task_id):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_1)
    cursor.execute(None, {'task_id': task_id})
    name_byte_array_id = []
    for res in cursor:
        name_byte_array_id.append(res)
    cursor.close()
    loop_var(name_byte_array_id)

def loop_var(name_id):
    for name, ba_id in name_id:
        print_var(name, ba_id)

def print_var(name, byte_array_id):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_2)
    cursor.execute(None, {'byte_array_id': byte_array_id})
    res = cursor.fetchone()
    if res is not None:
        blob_data = res[0]
        name = name + "_" + byte_array_id + ".ser"
        file = open(name, 'w')
        file.write(blob_data.read())
        file.close()
    cursor.close

def main():
    if len(sys.argv) != 3:
        print('usage: %s <connection string>' % sys.argv[0])
        sys.exit(1)

    db_connector.DBConnector(sys.argv[1])

    begin_print_var(sys.argv[2])

    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
