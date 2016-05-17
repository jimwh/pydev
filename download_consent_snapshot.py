#!/usr/bin/python

import os
import sys

from db import db_connector
from db import jproperties

SQL_CONSENT_SNAPSHOT_BY_ID = "\
select OID, CONSENTHEADEROID, FILECONTEXT, CREATIONDATE\
  from CONSENTSNAPSHOT where OID = :snapshot_id"


DIR_NAME = "/tmp/consent_snapshot/"


def download_consent_snapshot(snapshot_id):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_CONSENT_SNAPSHOT_BY_ID)
    cursor.execute(None, {'snapshot_id': snapshot_id})
    res = cursor.fetchone()

    if res is not None:
        print(res[3])
        creation_date = res[3]
        print(creation_date.strftime('%Y-%m-%d-%H-%M-%S'))

        if not os.path.exists(DIR_NAME):
            os.makedirs(DIR_NAME)

        file_name = DIR_NAME + '/cf_snapshot-' + str(res[0]) + '-' + str(res[1]) + '.pdf'

        try:
            file = open(file_name, 'w')
            file.write(res[2].read())
            file.close()
        except IOError:
            print('i/o error... {}'.format(file_name))

    cursor.close


def main():
    prop = jproperties.Properties()
    prop.load("./db/db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        return 1
    db_connector.DBConnector(connection_str)
    download_consent_snapshot(sys.argv[2])
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
    if len(sys.argv) != 3:
        print('usage: {} [prod|dev|staging|local] <snapshot_id>'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main())
