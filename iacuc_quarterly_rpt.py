#!/usr/bin/python

import sys

from db import db_connector
from db import jproperties

"""
select count(P.BUSINESS_KEY_) from ACT_HI_PROCINST P, ACT_HI_TASKINST T
where P.PROC_INST_ID_ = T.PROC_INST_ID_
and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'
and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
and trunc(to_date('08/27/2015', 'MM/DD/yyyy'));


select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
where P.PROC_INST_ID_ = T.PROC_INST_ID_
and T.TASK_DEF_KEY_='submit' and T.DELETE_REASON_='completed'
and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
and trunc(to_date('08/01/2015', 'MM/DD/yyyy'));


select P.BUSINESS_KEY_, T.END_TIME_
from ACT_HI_PROCINST P, ACT_HI_TASKINST T
where P.PROC_INST_ID_ = T.PROC_INST_ID_
and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'
and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
and trunc(to_date('08/01/2015', 'MM/DD/yyyy'))
and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where ProtocolYear='1' and modificationNumber='00');
"""



SQL_ID_AD_SD_DS = "\
select T1.IACUCPROTOCOLHEADERPER_OID, T1.STATUSCODEDATE approvalDate, T2.STATUSCODEDATE submitDate,\
trunc(T1.STATUSCODEDATE)-trunc(T2.STATUSCODEDATE) days from\
(\
   select * from (\
      select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE, ROW_NUMBER ()\
        OVER (PARTITION BY IACUCPROTOCOLHEADERPER_OID\
        ORDER BY STATUSCODEDATE DESC) rn from\
        (\
          select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
            where statuscode='Approve' and IACUCPROTOCOLHEADERPER_OID in\
              (\
                select distinct IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
                  where statuscode='Submit'\
                     and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
                     and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
              )\
              and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
              and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
        )\
   ) where rn = 1) T1,\
  (\
    select * from (\
      select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE, ROW_NUMBER ()\
        OVER (PARTITION BY IACUCPROTOCOLHEADERPER_OID\
        ORDER BY STATUSCODEDATE ASC) rn from\
        (\
          select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
            where statuscode='Submit'\
              and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
              and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
              and IACUCPROTOCOLHEADERPER_OID in (\
                select distinct IACUCPROTOCOLHEADERPER_OID from (\
                  select STATUSCODE, IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
                    where statuscode in ('Approve')\
                    and IACUCPROTOCOLHEADERPER_OID in (\
                      select IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
                        where statuscode='Submit'\
                          and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
                          and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
                    )\
                    and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
                    and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
                )\
              )\
            )\
        ) where rn=1) T2 \
  where T1.IACUCPROTOCOLHEADERPER_OID=T2.IACUCPROTOCOLHEADERPER_OID order by days"


# first submission id and date between April and July
SQL_FIRST_SUBMISSION_ID_DATE = "\
select * from (\
  select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE, ROW_NUMBER () OVER (PARTITION BY IACUCPROTOCOLHEADERPER_OID\
  ORDER BY STATUSCODEDATE ASC) rn from\
(\
  select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
    where statuscode='Submit'\
    and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
    and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
    and IACUCPROTOCOLHEADERPER_OID in (\
    select distinct IACUCPROTOCOLHEADERPER_OID from (\
      select STATUSCODE, IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
        where statuscode in ('Approve')\
          and IACUCPROTOCOLHEADERPER_OID in (\
          select IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
            where statuscode='Submit'\
              and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
              and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
          )\
    and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
    and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
  )\
)\
)\
) where rn=1"

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


SQL_APPROVAL_ID_DATE = "\
select * from (\
  select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE, ROW_NUMBER () OVER \
    (PARTITION BY IACUCPROTOCOLHEADERPER_OID ORDER BY STATUSCODEDATE DESC) rn from\
    (\
      select IACUCPROTOCOLHEADERPER_OID, STATUSCODEDATE from IACUCPROTOCOLSTATUS\
        where statuscode='Approve' and IACUCPROTOCOLHEADERPER_OID in\
          (\
           select distinct IACUCPROTOCOLHEADERPER_OID from IACUCPROTOCOLSTATUS\
           where statuscode='Submit'\
             and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
             and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
          )\
          and trunc(statusCodeDate) >= trunc(to_date('04/01/2015', 'MM/DD/yyyy'))\
          and trunc(statusCodeDate) <  trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
    )\
) where rn = 1"


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

def get_id_date(sql_state):
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(sql_state)
    oid_date = {}
    for res in cursor:
        oid_date[res[0]] = res[1]
    cursor.close()
    return oid_date

def get_id_adate_sdate_days():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_ID_AD_SD_DS)
    data_list = []
    for res in cursor:
        data_list.append(res)
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

    approval_count = get_total_approval_count()
    if approval_count is not None:
        print('total approval count={}'.format(approval_count))

    oid = get_header_id()
    print('number of header id: {}'.format(len(oid)))

    oid_approval_date = get_id_date(SQL_APPROVAL_ID_DATE)
    print('number of oid_approval_date: {}'.format(len(oid_approval_date)))
    # for key in oid_approval_date.keys():
    #    print('{}={}'.format(key, oid_approval_date[key]))

    oid_submit_date = get_id_date(SQL_FIRST_SUBMISSION_ID_DATE)
    # print('--- oid, submit date ---')
    # for key in oid_submit_date.keys():
    #    print('{}={}'.format(key, oid_submit_date[key]))
    print('number of oid_submit_date: {}'.format(len(oid_submit_date)))

    total_days = 0
    max_day = 0
    max_day_oid = None
    for header_id in oid:
        d = oid_approval_date[header_id].date() - oid_submit_date[header_id].date()
        # print('oid={}, days={}'.format(header_id, d.days))
        total_days += d.days
        if d.days > max_day:
            max_day = d.days
            max_day_oid = header_id

    data_list = get_id_adate_sdate_days()
    for data in data_list:
        print(data)
    close_db()
    print('avg={}, max days: {}, oid={}'.format(total_days/412, max_day, max_day_oid))
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())
