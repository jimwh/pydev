#!/usr/bin/python

import sys
import cx_Oracle
import db_connector
import jproperties


SQL_APPROVAL_ID_DATE = "\
  select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
  where trunc(statusCodeDate) between\
             trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
        and  trunc(to_date('06/30/2015', 'MM/DD/yyyy'))"

def get_approval_id_date():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_APPROVAL_ID_DATE)
    data_list = {}
    for res in cursor:
        data_list[res[0]] = res[1]
    cursor.close()
    return data_list

def open_db():
    prop = jproperties.Properties()
    prop.load("db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        return False
    db_connector.DBConnector(connection_str)
    return True

def close_db():
    db_connector.DBConnector.close()


def main():
    if open_db() is not True:
        return 1

    approval_id_date = get_approval_id_date()
    for data in approval_id_date:
        print(data)
    close_db()
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())
