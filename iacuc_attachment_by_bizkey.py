#!/usr/bin/python

import sys
import os
import cx_Oracle
import db_connector
#
# local:  rascal/rascal@127.0.0.1/XE
#
SQL_SELECT_STATMENT = "select A.NAME_, G.BYTES_ \
from ACT_HI_ATTACHMENT A inner join ACT_HI_TASKINST T on A.TASK_ID_ = T.ID_ \
inner join ACT_GE_BYTEARRAY G on G.ID_ = A.CONTENT_ID_ \
inner join ACT_HI_PROCINST P on T.PROC_INST_ID_=P.PROC_INST_ID_ \
where P.BUSINESS_KEY_ = :bizkey"


def download_attachment(bizkey):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_SELECT_STATMENT)
    cursor.execute(None, {'bizkey': bizkey})

    dirname = "/tmp/iacuc/" + bizkey
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for res in cursor:
        (name, blob_data) = res
        filename = "/".join((dirname, name))
        try:
            file = open(filename, 'w')
            file.write(blob_data.read())
            file.close()
        except IOError:
            print('i/o error... %s' % filename)

    if cursor.rowcount == 0:
        print('no result for headerId=%s' % bizkey)
    else:
        print('number of items: %d' % cursor.rowcount)
    cursor.close()


def main():
    if len(sys.argv) != 3:
        print('usage: %s <connection string> <headerId>' % sys.argv[0])
        sys.exit(1)

    db_connector.DBConnector(sys.argv[1])
    download_attachment(sys.argv[2])
    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
