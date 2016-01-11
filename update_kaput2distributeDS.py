#!/usr/bin/python

import sys

from db import db_connector
from db import jproperties

SQL_TASK_ID = "select HT.ID_\
  from ACT_HI_TASKINST HT, ACT_HI_PROCINST HP, IACUCPROTOCOLSTATUS S\
  where HT.task_def_key_='kaput'\
  and HT.PROC_DEF_ID_ like 'IacucApprov%'\
  and HT.PROC_INST_ID_ = HP.PROC_INST_ID_\
  and HT.DELETE_REASON_='completed'\
  and S.IACUCPROTOCOLHEADERPER_OID = HP.BUSINESS_KEY_\
  and S.STATUSCODEDATE = HT.END_TIME_\
  and trunc(S.STATUSCODEDATE) >= trunc(to_date('01/01/2013', 'MM/DD/YYYY'))\
  and S.STATUSCODE='Distribute'\
  order by HT.ID_ desc"

SQL_UPDATE = "update ACT_HI_TASKINST\
    set TASK_DEF_KEY_='distributeToDS', NAME_='Distribute: Designated Reviewers'\
    where ID_= :task_id and TASK_DEF_KEY_='kaput'"


def update_kaput2submit(task_id):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_UPDATE)
    cursor.execute(None, {'task_id': task_id})
    db_connector.DBConnector.commit()
    cursor.close()


def get_task_id():
    task_id = []
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_TASK_ID)
    for res in cursor:
        task_id.append(res[0])
    cursor.close()
    return task_id


def main():
    prop = jproperties.Properties()
    prop.load("./db/db.properties")
    if len(sys.argv) == 1:
        print('Usage: %s <connection string>' % sys.argv[0])
        sys.exit(1)

    connection_str = prop.get(sys.argv[1])
    if connection_str is None:
        print('No connection string defined')
        sys.exit(1)

    db_connector.DBConnector(connection_str)

    task_id_list = get_task_id()
    print("listSize=%d" % len(task_id_list))

    for task_id in task_id_list:
        print("id=%s" % task_id)
        update_kaput2submit(task_id)

    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    main()


# =AVERAGEIF($Sheet1.$A$2:$A$4722,A59,$Sheet1.$M$2:$Sheet1.$M$4722)

# =AVERAGEIF($Sheet1.$A$2:$A$5145,A60,$Sheet1.$M$2:$Sheet1.$M$5145)