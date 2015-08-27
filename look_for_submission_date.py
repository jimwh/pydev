#!/usr/bin/python

import sys
import cx_Oracle
import db_connector
import jproperties

SQL_APPROVAL_ID_DATE = "\
  select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS \
  where trunc(statusCodeDate) \
  between trunc(to_date('04/01/2015', 'MM/DD/yyyy')) and  trunc(to_date('06/30/2015', 'MM/DD/yyyy')) \
  and statusCode='Done'"

SQL_STATUS_BY_ID = "\
  select STATUSCODE, STATUSCODEDATE from IACUCPROTOCOLSTATUS \
  where IACUCPROTOCOLHEADERPER_OID = :header_id \
  and statusCode not in('Create', 'Done')\
  order by STATUSCODEDATE asc"

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

def get_submission_date(header_id):

    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_STATUS_BY_ID)
    cursor.execute(None, {'header_id': header_id})

    submission_date = None
    for res in cursor:
        # print(res)
        if res[0] == 'Submit':
            submission_date = res[1]
            cursor.close()
            return submission_date

    cursor.close()
    return submission_date

def get_approval_id_submission_date(header_id_list):
    id_date = {}
    for header_id in header_id_list:
        submission_date = get_submission_date(header_id)
        if submission_date is not None:
            id_date[header_id] = submission_date

    return id_date

def main():
    if open_db() is not True:
        return 1

    approval_id_date = get_approval_id_date()
    print('num of approvals: {}'.format(len(approval_id_date)))
    id_submission_date = get_approval_id_submission_date(approval_id_date.keys())
    close_db()

    for key in approval_id_date.keys():
        dd = approval_id_date[key].date() - id_submission_date[key].date()
        print('header_id={}, d1={}, d2={}, days={}'.format(key, approval_id_date[key], id_submission_date[key], dd.days))

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())
