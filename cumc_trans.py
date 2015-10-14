#!/usr/bin/python

import sys

from db import db_connector
from db import jproperties

"""
1. rascal consent forms
2. attached consent forms
3. attached standard alone protocols
"""
# -- step 1.  approved active protocol headerId, protocolNumber, protocolYear, protocolModificationNumber
SQL_PROTOCOL_INFO = "\
select H.OID headerId, P.PROTOCOLNUMBER, H.PROTOCOLYEAR, H.MODIFICATIONNUMBER\
  from IRBPROTOCOLHEADER H\
  join IRBPROTOCOL P on P.OID = H.PARENTPROTOCOLOID\
  join IRBSTATUS S on S.PARENTOBJECTOID=H.OID\
  where\
  H.OID = (select max(iph.OID) from IrbProtocolHeader iph where iph.PARENTPROTOCOLOID = H.PARENTPROTOCOLOID) and\
  H.IRBAPPROVALDATE is not null and\
  S.STATUSNAME='Approved' and\
  trunc(H.EXPIRATIONDATE) >= trunc(sysdate) and\
  P.PROTOCOLNUMBER in(\
  'AAAN6059','AAAA9305','AAAB8464','AAAC1962','AAAD5487','AAAE9695','AAAF4253','AAAI0804','AAAJ4751','AAAK5904','AAAN0105')\
  order by H.IRBAPPROVALDATE desc"

SQL_RASCAL_CONSENT_FORM = "\
select ch.IRBPROTOCOLHEADERID, ch.CONSENTNUMBER, dh.FILECONTEXT\
  from CONSENTHEADER ch, CONSENTDATASHEET dh\
  where ch.OID = dh.CONSENTHEADEROID and\
  ch.IRBPROTOCOLHEADERID = dh.IRBPROTOCOLHEADEROID and\
  ch.IRBPROTOCOLHEADERID in(\
    230962, 229301, 226399, 226240, 223935, 218756, 218164, 217850, 213667)\
  and ch.OID = (select max(c.OID) from CONSENTHEADER c where c.CONSENTNUMBER=ch.CONSENTNUMBER)\
  and dh.OID = (select max(d.OID) from CONSENTDATASHEET d where d.CONSENTHEADEROID=ch.OID)"

def dump_rascal_consent_form(oid_num):
    print(oid_num)
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_RASCAL_CONSENT_FORM)
    for res in cursor:
        print(res)
        file_name = 'CF-' + res[1] + '.pdf'
        print(file_name)
        try:
            file = open(file_name, 'w')
            file.write(res[2].read())
            file.close()
        except IOError:
            print('i/o error... {}'.format(file_name))

    cursor.close


def protocol_info():
    protocol = []
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_PROTOCOL_INFO)
    for res in cursor:
        protocol.append(res)
        print(res[1] + '_Y' + str(res[2]) + '_M' + str(res[3]))

    cursor.close
    return protocol


def main():
    prop = jproperties.Properties()
    prop.load("./db/db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        return 1

    db_connector.DBConnector(connection_str)
    protocol = protocol_info()
    print(protocol)
    oid_num = {}
    for protocolInfo in protocol:
        oid, num, yy, mod = protocolInfo
        oid_num[oid] = num
    dump_rascal_consent_form(oid_num)

    db_connector.DBConnector.close()
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())

