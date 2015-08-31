#!/usr/bin/python

import sys

import db_connector
import jproperties


SQL_SELECT_BY_PROTOCOL_NUM="\
select H.OID, P.PROTOCOLNUMBER, H.PROTOCOLYEAR, H.MODIFICATIONNUMBER,\
  T.ID snapshotId, T.SNAPSHOT,\
  S.OID statusId,\
  H.OID headerId, IRBAPPROVALDATE, EXPIRATIONDATE, S.STATUSDATE \
from IRBPROTOCOLHEADER H \
join IRBPROTOCOL P on H.PARENTPROTOCOLOID=P.OID \
join IRBSTATUS S on S.PARENTOBJECTOID=H.OID \
join IRBPROTOCOLSNAPSHOT T on T.IRBSTATUSID=S.OID \
where \
H.OID = (select max(OID) from IrbProtocolHeader iph where iph.PARENTPROTOCOLOID = H.PARENTPROTOCOLOID) and \
H.IRBAPPROVALDATE is not null and \
S.STATUSNAME='Approved' and \
P.PROTOCOLNUMBER= :protocol_num"

def download_protocol(protocol_num):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_SELECT_BY_PROTOCOL_NUM)
    cursor.execute(None, {'protocol_num': protocol_num})
    res = cursor.fetchone()

    if res is not None:
        print(res)
        file_name = protocol_num + '_Y' + str(res[2]) + '_M' + str(res[3]) + '.pdf'
        try:
            file = open(file_name, 'w')
            file.write(res[5].read())
            file.close()
        except IOError:
            print('i/o error... {}'.format(file_name))

    cursor.close

def main():
    prop = jproperties.Properties()
    prop.load("../db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        return 1
    db_connector.DBConnector(connection_str)
    download_protocol('AAAP7757')
    db_connector.DBConnector.close()
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())

