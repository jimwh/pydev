#!/usr/bin/python

import os
import sys
import zipfile
import time

from db import db_connector
from db import jproperties

SQL_RASCAL_CONSENT_FORM = "\
select CH.CONSENTNUMBER, CD.CONSENTHEADEROID, CD.FILECONTEXT,\
  H.OID headerId, P.PROTOCOLNUMBER, H.PROTOCOLYEAR, H.MODIFICATIONNUMBER\
  from IRBPROTOCOLHEADER H\
  join IRBPROTOCOL P on H.PARENTPROTOCOLOID=P.OID\
  join IRBSTATUS S on S.PARENTOBJECTOID=H.OID\
  join CONSENTDATASHEET CD on CD.IRBPROTOCOLHEADEROID = H.OID\
  join CONSENTHEADER CH on CH.IRBPROTOCOLHEADERID = H.OID\
  where\
  H.OID = (select max(iph.OID) from IrbProtocolHeader iph where iph.PARENTPROTOCOLOID = H.PARENTPROTOCOLOID) and\
  S.OID = (select max(ss.OID) from IrbStatus ss where ss.PARENTOBJECTOID=H.OID) and\
  H.IRBAPPROVALDATE is not null and\
  trunc(H.EXPIRATIONDATE) >= trunc(sysdate) and\
  S.STATUSNAME='Approved' and\
  P.PROTOCOLNUMBER in ('AAAN6059','AAAA9305','AAAB8464',\
                     'AAAC1962','AAAD5487','AAAE9695','AAAF4253','AAAI0804',\
                     'AAAJ4751','AAAK5904','AAAN0105')\
  order by H.IRBAPPROVALDATE desc"


DIR_NAME = "/tmp/cumc/"


def download_rascal_consent_form():
    cursor = db_connector.DBConnector.cursor()
    cursor.execute(SQL_RASCAL_CONSENT_FORM)

    for res in cursor:
        protocol_num = '{}_Y{:02}_M{:02}'.format(res[4], res[5], res[6])
        print(protocol_num)
        dir_name = DIR_NAME + '/' + protocol_num + '/RASCAL_CONSENT_FORMS'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        file_name = dir_name + '/CF-' + res[0] + '.pdf'

        if res[2] is not None:
            dump_to_file(file_name, res[2])

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

    download_rascal_consent_form()

    db_connector.DBConnector.close()

    return 0

"""
    zip_file_name = '/tmp/rascal_to_cumc_' + time.strftime('%Y%m%d') + '.zip'
    zf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    os.chdir("/tmp")
    for dirname, subdirs, files in os.walk("./cumc"):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
"""

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} [prod|dev|staging|local]'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())


