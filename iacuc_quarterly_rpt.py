#!/usr/bin/python

import sys
import cx_Oracle
import db_connector
import jproperties

# --, 'Done')
SQL_APPROVAL_COUNT = "\
select count(distinct IACUCPROTOCOLHEADERPER_OID) from \
(\
    select STATUSCODE, IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
    where statuscode in ('Approve')\
and IACUCPROTOCOLHEADERPER_OID in (\
    select IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
    where statuscode='Submit'\
                     and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy')\
                     and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy')\
)\
and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy') \
and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy') \
) S1 "

SQL_HEADER_ID = "select distinct IACUCPROTOCOLHEADERPER_OID from\
(\
    select STATUSCODE, IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
    where statuscode in ('Approve')\
and IACUCPROTOCOLHEADERPER_OID in (\
    select IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
    where statuscode='Submit'\
                     and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy')\
                     and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy')\
)\
and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy') \
and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy') \
) S1 order by IACUCPROTOCOLHEADERPER_OID"

SQL_APPROVAL_ID_DATE = "select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS \
where statuscode='Approve' and IACUCPROTOCOLHEADERPER_OID in (\
    select IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
    where statuscode='Submit'\
                     and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy')\
                     and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy')\
)\
and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy') \
and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy') \
order by IACUCPROTOCOLHEADERPER_OID"

SQL_ID_SUBMIT_DATE="select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS \
where statuscode='Submit'\
and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy') \
and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy') \
and IACUCPROTOCOLHEADERPER_OID in (\
    select distinct IACUCPROTOCOLHEADERPER_OID from (\
    select STATUSCODE, IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
    where statuscode in ('Approve')\
          and IACUCPROTOCOLHEADERPER_OID in (\
    select IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
    where statuscode='Submit'\
                     and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy')\
                     and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy')\
)\
and trunc(statusCodeDate) >= to_date('04/01/2015', 'MM/DD/yyyy')\
    and trunc(statusCodeDate) < to_date('07/01/2015', 'MM/DD/yyyy')\
)\
) order by IACUCPROTOCOLSTATUS.IACUCPROTOCOLHEADERPER_OID"


def get_total_approval_count():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_APPROVAL_COUNT)
    res = cursor.fetchone()
    count = None
    if res is not None:
        count = res[0]
    cursor.close()
    return count

def get_header_id():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_HEADER_ID)
    header_id = []
    for res in cursor:
        header_id.append(res[0])
    cursor.close()
    return header_id

def get_header_id_date():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_APPROVAL_ID_DATE)
    oid_date = {}
    for res in cursor:
        oid_date[res[0]] = res[1]
    cursor.close()
    return oid_date

def get_header_id_submit_date():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_ID_SUBMIT_DATE)
    oid_date = {}
    for res in cursor:
        oid, submit_date = res[0], res[1]
        if oid not in oid_date:
            oid_date[oid] = submit_date
        else:
            if oid_date[oid] > submit_date:
                print('oid={}, d1={}, d2={}'.format(oid, oid_date[oid], submit_date))
                oid_date[oid] = submit_date
    cursor.close()
    return oid_date

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

    approval_count = get_total_approval_count()
    if approval_count is not None:
        print('total approval count={}'.format(approval_count))

    oid = get_header_id()
    print('number of header id: {}'.format(len(oid)))

    oid_approval_date = get_header_id_date()
    print('number of id_date: {}'.format(len(oid_approval_date)))
    for key in oid_approval_date.keys():
        print('{}={}'.format(key, oid_approval_date[key]))

    oid_submit_date = get_header_id_submit_date();
    print('--- oid, submit date ---')
    for key in oid_submit_date.keys():
        print('{}={}'.format(key, oid_submit_date[key]))

    print('number of oid_submit_date: {}'.format(len(oid_submit_date)))

    total_days = 0
    max_day = 0
    max_day_oid = None
    for header_id in oid:
        d = oid_approval_date[header_id].date() - oid_submit_date[header_id].date()
        print('oid={}, days={}'.format(header_id, d.days))
        total_days += d.days
        if d.days > max_day:
            max_day = d.days
            max_day_oid = header_id
    close_db()
    print('avg={}, max days: {}, oid={}'.format(total_days/412, max_day, max_day_oid))
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())
