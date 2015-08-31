#!/usr/bin/python

import sys

import db_connector
import jproperties
import javaobj

"""
select STDDEV(days) from
(
  select  T1.BUSINESS_KEY_, trunc(T1.END_TIME_)-trunc(T2.END_TIME_) days from
  (
    select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
    where P.PROC_INST_ID_ = T.PROC_INST_ID_
    and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'
    and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
    and trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
    and P.BUSINESS_KEY_<> 80604
    and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where ProtocolYear='1' and modificationNumber='00')
  ) T1,
  (
  select * from (
    select BUSINESS_KEY_, END_TIME_, ROW_NUMBER ()
          OVER (PARTITION BY BUSINESS_KEY_ ORDER BY END_TIME_ asc) rn
    from
    (
      select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
      where P.PROC_INST_ID_ = T.PROC_INST_ID_
      and T.TASK_DEF_KEY_='submit' and T.DELETE_REASON_='completed'
      and trunc(T.END_TIME_) <= trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
      and BUSINESS_KEY_<> 80604
      and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where ProtocolYear='1' and modificationNumber='00')
    )
  )
  where rn=1
  ) T2
  where T1.BUSINESS_KEY_=T2.BUSINESS_KEY_
)


select * from IACUCPROTOCOLSTATUS where IACUCPROTOCOLHEADERPER_OID=80604
order by statuscodedate desc;


select 1, 'Volume of Approvals' Title, count(*) DAYS from ACT_HI_TASKINST
where TASK_DEF_KEY_='finalApproval' and DELETE_REASON_='completed'
and trunc(END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
and trunc(to_date('08/27/2015', 'MM/DD/yyyy'))

UNION

select 2, 'Average from Submission to Approval', round(avg(days)) from
(
  select  T1.BUSINESS_KEY_, trunc(T1.END_TIME_)-trunc(T2.END_TIME_) days from
  (
    select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
    where P.PROC_INST_ID_ = T.PROC_INST_ID_
    and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'
    and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
    and trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
    and P.BUSINESS_KEY_<> 80604
    and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where ProtocolYear='1' and modificationNumber='00')
  ) T1,
  (
  select * from (
    select BUSINESS_KEY_, END_TIME_, ROW_NUMBER ()
          OVER (PARTITION BY BUSINESS_KEY_ ORDER BY END_TIME_ asc) rn
    from
    (
      select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
      where P.PROC_INST_ID_ = T.PROC_INST_ID_
      and T.TASK_DEF_KEY_='submit' and T.DELETE_REASON_='completed'
      and trunc(T.END_TIME_) <= trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
      and BUSINESS_KEY_<> 80604
      and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where ProtocolYear='1' and modificationNumber='00')
    )
  )
  where rn=1
  ) T2
  where T1.BUSINESS_KEY_=T2.BUSINESS_KEY_
)

UNION

select 3, 'Median from Submission to Approval', median(days) from
(
  select trunc(T1.END_TIME_)-trunc(T2.END_TIME_) days from
  (
    select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
    where P.PROC_INST_ID_ = T.PROC_INST_ID_
    and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'
    and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
    and trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
    and BUSINESS_KEY_<> 80604
    and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where ProtocolYear='1' and modificationNumber='00')
  ) T1,
  (
  select * from (
    select BUSINESS_KEY_, END_TIME_, ROW_NUMBER ()
          OVER (PARTITION BY BUSINESS_KEY_ ORDER BY END_TIME_ asc) rn
    from
    (
      select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
      where P.PROC_INST_ID_ = T.PROC_INST_ID_
      and T.TASK_DEF_KEY_='submit' and T.DELETE_REASON_='completed'
      and trunc(T.END_TIME_) <= trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
      and BUSINESS_KEY_<> 80604
      and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where ProtocolYear='1' and modificationNumber='00')
    )
  )
  where rn=1
  ) T2
  where T1.BUSINESS_KEY_=T2.BUSINESS_KEY_
)

UNION

select 4, 'Average BC from Submission to Approval', round(avg(days)) from
(
  select trunc(T1.END_TIME_)-trunc(T2.END_TIME_) days from
  (
    select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
    where P.PROC_INST_ID_ = T.PROC_INST_ID_
    and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'
    and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
    and trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
    and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where PAINCATEGORY1='Y' or PAINCATEGORY2='Y')
  ) T1,
  (
  select * from (
    select BUSINESS_KEY_, END_TIME_, ROW_NUMBER ()
          OVER (PARTITION BY BUSINESS_KEY_ ORDER BY END_TIME_ asc) rn
    from
    (
      select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
      where P.PROC_INST_ID_ = T.PROC_INST_ID_
      and T.TASK_DEF_KEY_='submit' and T.DELETE_REASON_='completed'
      and trunc(T.END_TIME_) <= trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
      and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where PAINCATEGORY1='Y' or PAINCATEGORY2='Y')
    )
  )
  where rn=1
  ) T2
  where T1.BUSINESS_KEY_=T2.BUSINESS_KEY_
)

UNION

select 5, 'Average DE from Submission to Approval', round(avg(days)) from
(
  select trunc(T1.END_TIME_)-trunc(T2.END_TIME_) days from
  (
    select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
    where P.PROC_INST_ID_ = T.PROC_INST_ID_
    and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'
    and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))
    and trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
    and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where PAINCATEGORY3='Y' or PAINCATEGORY4='Y')
  ) T1,
  (
  select * from (
    select BUSINESS_KEY_, END_TIME_, ROW_NUMBER ()
          OVER (PARTITION BY BUSINESS_KEY_ ORDER BY END_TIME_ asc) rn
    from
    (
      select P.BUSINESS_KEY_, T.END_TIME_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T
      where P.PROC_INST_ID_ = T.PROC_INST_ID_
      and T.TASK_DEF_KEY_='submit' and T.DELETE_REASON_='completed'
      and trunc(T.END_TIME_) <= trunc(to_date('08/27/2015', 'MM/DD/yyyy'))
      and P.BUSINESS_KEY_ in (select OID from IacucProtocolHeader where PAINCATEGORY3='Y' or PAINCATEGORY4='Y')
    )
  )
  where rn=1
  ) T2
  where T1.BUSINESS_KEY_=T2.BUSINESS_KEY_
);
"""

SQL_SUBMIT_TASKID="select A.TASKID_, O.STATUSCODE from IACUC_MIGRATOR A, IACUCPROTOCOLSTATUS O\
 where a.STATUSID_=O.OID and O.STATUSCODE='Submit'\
 and A.TASKID_ in (\
    select ID_ from (\
      select T.PROC_INST_ID_, T.ID_, T.TASK_DEF_KEY_ from ACT_HI_TASKINST T\
        where T.TASK_DEF_KEY_='kaput' and\
              T.PROC_INST_ID_ in(\
                select PROC_INST_ID_ from ACT_HI_PROCINST\
                  where BUSINESS_KEY_ in (\
                        select BUSINESS_KEY_ from\
                        (\
                         select P.BUSINESS_KEY_, P.PROC_INST_ID_ from ACT_HI_PROCINST P, ACT_HI_TASKINST T\
                            where P.PROC_INST_ID_ = T.PROC_INST_ID_\
                                  and T.TASK_DEF_KEY_='finalApproval' and T.DELETE_REASON_='completed'\
                                  and trunc(T.END_TIME_) between trunc(to_date('07/01/2015', 'MM/DD/yyyy'))\
                                  and trunc(to_date('08/29/2015', 'MM/DD/yyyy'))\
                                  order by P.BUSINESS_KEY_\
                        )\
                )\
      )\
    )\
)"

SQL_HI_DETAIL = "\
    select bytes_ from ACT_GE_BYTEARRAY where ID_= (\
      select BYTEARRAY_ID_ from ACT_HI_DETAIL where TASK_ID_ = :task_id)"

SQL_UPDATE = "\
    update ACT_HI_TASKINST set TASK_DEF_KEY_='submit', NAME_='Submit'\
    where ID_ = :task_id and TASK_DEF_KEY_='kaput'"

def print_detail(task_id):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_HI_DETAIL)
    cursor.execute(None, {'task_id': task_id})
    res = cursor.fetchone()

    if res is not None:
        blob_data = res[0]
        pobj = javaobj.loads(blob_data.read())
        print(pobj)

    cursor.close


def get_submission_task_id():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_SUBMIT_TASKID)
    data_list = []
    for res in cursor:
        data_list.append(res[0])
    cursor.close()
    return data_list


def update_kaput_to_submit(task_id):

    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_UPDATE)
    cursor.execute(None, {'task_id': task_id})
    db_connector.DBConnector.commit()
    cursor.close()


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

    submission_task_id = get_submission_task_id()
    print('num of submission: {}'.format(len(submission_task_id)))

    for task_id in submission_task_id:
        print('task_id={}'.format(task_id))
        # print_detail(task_id)
        update_kaput_to_submit(task_id)

    close_db()
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())
