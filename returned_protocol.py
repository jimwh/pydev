#!/usr/bin/python

import sys
import cx_Oracle
import db_connector

sql_protocol_num_list = "select OID, PROTOCOLNUMBER, PROTOCOLYEAR, MODIFICATIONNUMBER from IACUCPROTOCOLHEADER where CURRENTSTATUS='ReturnToPI' order by OID"

sql_end_time = "select max(end_time_) from ACT_HI_TASKINST \
where PROC_INST_ID_ in (\
select PROC_INST_ID_ from ACT_HI_PROCINST where PROC_DEF_ID_ like 'Iacuc%' and BUSINESS_KEY_= :bizkey) \
and ACT_HI_TASKINST.TASK_DEF_KEY_='returnToPI' \
order by end_time_ desc"

sql_get_task_id = "select ID_ from\
(select * from ACT_HI_TASKINST where PROC_INST_ID_ in(\
select ID_ from ACT_HI_PROCINST where BUSINESS_KEY_= :bizkey) \
order by ACT_HI_TASKINST.END_TIME_ desc) T \
where ROWNUM=1"

sql_update_kaput = "update ACT_HI_TASKINST set TASK_DEF_KEY_='returnToPI', NAME_='Return to PI' \
where ID_= :task_id and TASK_DEF_KEY_='kaput'"

def update_kaput(task_id):
    print("kaput task_id: %s" % task_id)
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(sql_update_kaput)
    cursor.execute(None, {'task_id': task_id})
    db_connector.DBConnector.commit()
    cursor.close

def get_task_id(bizkey):
    print('bizkey=%s' % bizkey)
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(sql_get_task_id)
    cursor.execute(None, {'bizkey': bizkey})
    task_id = cursor.fetchone()
    cursor.close
    return task_id[0]


def get_protocol_list():
    protocol_dict = {}
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(sql_protocol_num_list)
    for res in cursor:
        protocol_dict[res[0]] = (res[1], res[2], res[3])
    cursor.close()
    return protocol_dict

def get_end_time(bizkey):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(sql_end_time)
    cursor.execute(None, {'bizkey': bizkey})
    res = cursor.fetchone()
    cursor.close
    return res[0]

def get_returned_numbers():
    protocol_dict = get_protocol_list()
    print("number of returned protocols: %d" % (len(protocol_dict)))
    # have to return a new dict for modified tuples
    item_dict = {}
    not_found_list = []
    for key in sorted(protocol_dict.keys()):
        end_time = get_end_time(key)
        item = protocol_dict[key]
        if end_time is not None:
            end_time_string = end_time.strftime("%Y-%m-%d %H:%M:%S")
            item += (end_time_string,)
            protocol_dict[key] = item
            item_dict[key] = item
        else:
            not_found_list.append(key)
            print("no end_time for OID=%s, PROTOCOLNUMBER=%s" % (key, item[0]))
    return item_dict, not_found_list

def main():
    if len(sys.argv) != 2:
        print('usage: %s <connection string>' % sys.argv[0])
        sys.exit(1)

    db_connector.DBConnector(sys.argv[1])

    protocol_dict, not_found_list = get_returned_numbers()
    print("final list of number of returned protocols: %s" % (len(protocol_dict)))

    print("not found list: %s" % len(not_found_list))
    for oid in not_found_list:
        task_id = get_task_id(oid)
        print('task_id=%s' % task_id)
        ### update_kaput(task_id)

    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
