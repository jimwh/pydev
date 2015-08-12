#!/usr/bin/python

import sys
import cx_Oracle

sql_protocol_num_list = "select OID, PROTOCOLNUMBER, PROTOCOLYEAR, MODIFICATIONNUMBER from IACUCPROTOCOLHEADER where CURRENTSTATUS='ReturnToPI' order by OID";

connection = ''
connection_string = ''

sql_end_time = "select max(end_time_) from ACT_HI_TASKINST where PROC_INST_ID_ in (\
select PROC_INST_ID_ from ACT_HI_PROCINST where PROC_DEF_ID_ like 'Iacuc%' and \
ACT_HI_TASKINST.TASK_DEF_KEY_ in('returnToPI', 'kaput') \
and BUSINESS_KEY_='FOO') order by end_time_ desc";

def get_protocol_list():
    protocol_dict = {}
    cursor = connection.cursor()
    cursor.execute(sql_protocol_num_list)
    for res in cursor:
        protocol_dict[res[0]] = (res[1], res[2], res[3])
    cursor.close()
    return protocol_dict

def get_end_time(line):
    cursor = connection.cursor()
    cursor.execute(line)
    end_time = ''
    for res in cursor:
        end_time = res[0]
    cursor.close()
    return end_time


def get_returned_numbers():
    global connection
    global connection_string

    connection = cx_Oracle.connect(connection_string)

    protocol_dict = get_protocol_list()
    print("number of returned protocols: %d" % (len(protocol_dict)))
    # have to return a new dict for modified tuples
    item_dict = {}
    for key in sorted(protocol_dict.keys()):
        line = sql_end_time.replace('FOO', str(key))
        end_time = get_end_time(line)
        item = protocol_dict[key]
        if end_time is not None:
            end_time_string = end_time.strftime("%Y-%m-%d %H:%M:%S")
            item += (end_time_string,)
            protocol_dict[key] = item
            item_dict[key] = item
        else:
            print("-------------------------------no time for OID=%s, PROTOCOLNUMBER=%s" % (key, item[0]))
    connection.close()
    return item_dict

def main():
    if len(sys.argv) != 2:
        print('usage: ./returned_protocol.py <connection string>')
        sys.exit(1)
    global connection_string
    connection_string = sys.argv[1]
    protocol_dict = get_returned_numbers()
    print("final list of number of returned protocols: %s" %(len(protocol_dict)))
    for key in sorted(protocol_dict.keys()):
        (protocol_num, yr, mod_num, returned_date) = protocol_dict[key]
        print("%s, %s, %s, %s" % (protocol_num, yr, mod_num, returned_date))

if __name__ == '__main__':
    main()
