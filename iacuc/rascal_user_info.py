#!/usr/bin/python

import sys

from iacuc import db_connector, jproperties

SQL_SELECT_STATEMENT = "\
select distinct 'IRB', p.OID, p.PROTOCOLNUMBER,to_char(h.CREATIONDATE, 'MM/DD/YYYY') \
from IRBPROTOCOL p, IRBPROTOCOLHEADER h, IRBSTAFF s \
where p.OID=h.PARENTPROTOCOLOID and s.RID= :rid and h.OID=s.IRBPROTOCOLHEADERID \
AND h.OID=(select max(OID) from IRBPROTOCOLHEADER where PARENTPROTOCOLOID=p.OID) \
UNION \
select distinct 'IACUC', h.OID, h.protocolnumber, to_char(h.CREATEDATE, 'MM/DD/YYYY') \
from IACUCSTAFF s, IACUCPROTOCOLHEADER h \
where s.rid= :rid and s.IACUCPROTOCOLHEADERPER_OID=h.OID \
UNION \
select 'PROPOSAL', h.OID, h.trakid, to_char(h.CREATIONDATE, 'MM/DD/YYYY') \
from PTPROPOSALHEADER h, PTACCESSCONTROL a \
WHERE a.RID= :rid and a.PT_HEADER_ID = h.OID \
UNION \
select 'TRAINING', uh.OID, ch.COURSENUMBER, to_char(uh.DATEPASSED, 'MM/DD/YYYY') \
from TCUSERHEADER uh, TCCOURSEHEADER ch \
where   rid= :rid and uh.TC_COURSEHEADER_ID=ch.oid \
order by 1, OID DESC"

SQL_GET_RID = "select rid from RASCAL_USER where USER_ID= :uni"

def get_rid(uni):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_GET_RID)
    cursor.execute(None, {'uni': uni})
    res = cursor.fetchone()
    if not res:
        cursor.close()
        return
    rid = res[0]
    cursor.close()
    return rid

def print_by_rid(rid):
    cursor = db_connector.DBConnector.cursor()
    cursor.prepare(SQL_SELECT_STATEMENT)
    cursor.execute(None, {'rid': rid})
    for res in cursor:
        print(res)
    cursor.close()

def main():
    prop = jproperties.Properties()
    prop.load("db.properties")
    connection_str = prop.get(sys.argv[1])
    if not connection_str:
        print('error: connection string undefined')
        sys.exit(1)

    db_connector.DBConnector(connection_str)
    rid = get_rid(sys.argv[2])
    if rid is None:
        print('not found rid for uni={}'.format(sys.argv[2]))
        db_connector.DBConnector.close()
        sys.exit(0)
    print_by_rid(rid)
    db_connector.DBConnector.close()
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        # print('usage: %s [prod|dev|staging|local] <uni>' % sys.argv[0])
        print('usage: {} [prod|dev|staging|local] <uni>'.format(sys.argv[0]))
        sys.exit(1)
    main()
