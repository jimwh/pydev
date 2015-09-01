#!/usr/bin/python

import os
import sys

from db import db_connector
from db import jproperties

SQL_STANDALONE_PROTOCOL = "\
select H.OID, P.PROTOCOLNUMBER, H.protocolYear, H.modificationnumber,\
    A.FILENAME, A.DOCUMENTDATA, A.DOCUMENTDATASTAMPED, A.DOCUMENTIDENTIFIER \
from IRBPROTOCOLHEADER H \
  join IRBPROTOCOL P on H.PARENTPROTOCOLOID=P.OID \
  join IRBSTATUS S on S.PARENTOBJECTOID=H.OID \
  join IRBATTACHMENT A on A.IRBPROTOCOLHEADERID=H.OID \
where\
  H.OID = (select max(iph.OID) from IrbProtocolHeader iph\
    where iph.PARENTPROTOCOLOID = H.PARENTPROTOCOLOID) and\
  S.OID = (select max(ss.OID) from IrbStatus ss where ss.PARENTOBJECTOID=H.OID) and\
  H.IRBAPPROVALDATE is not null and\
  trunc(H.EXPIRATIONDATE) >= trunc(sysdate) and\
  S.STATUSNAME='Approved' and\
  A.ATTACHMENTTYPECODE=8 and\
  A.ARCHIVE='N' and A.ACTIVE='Y' \
  and P.PROTOCOLNUMBER='AAAJ7852'"

DIR_NAME = "/tmp/cumc/"

def download_protocol():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_STANDALONE_PROTOCOL)

    for res in cursor:
        protocol_num = '{}_Y{:02}_M{:02}'.format(res[1], res[2], res[3])
        print(protocol_num)
        dir_name = DIR_NAME + '/' + protocol_num + '/ATTACHED_STANDALONE_PROTOCOLS'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        file_name = dir_name + '/' + res[4]

        if res[6] is not None:
            dump_to_file(file_name, res[6])
        else:
            dump_to_file(file_name, res[5])

    cursor.close

def dump_to_file(file_name, blob_data):

    try:
        file = open(file_name, 'w')
        file.write(blob_data.read())
        file.close()
    except IOError:
        print('i/o error... {}'.format(file_name))


def main():
    prop = jproperties.Properties()
    prop.load("./db/db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        return 1
    db_connector.DBConnector(connection_str)
    download_protocol()
    db_connector.DBConnector.close()
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())

