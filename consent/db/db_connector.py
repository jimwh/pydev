#!/usr/bin/python

import cx_Oracle


class DBConnector:
    instance = None

    class Connector:
        def __init__(self, connection_str):
            self.connection_str = connection_str
            self.error_msg = 'no error'
            self.error_code = 0
            self.connection = cx_Oracle.connect(connection_str)
            print(connection_str)

        def __str__(self):
            return repr(self) + self.connection_str

        def version(self):
            return self.connection.version.split(".")

        def get_cursor(self):
            return self.connection.cursor()

        def commit(self):
            self.connection.commit()

        def close(self):
            self.connection.close()

    def __init__(self, connection_str):
        if not DBConnector.instance:
            DBConnector.instance = DBConnector.Connector(connection_str)
        else:
            DBConnector.instance.connection_str = connection_str

    def get_cursor(self):
        return DBConnector.instance.self.get_cursor()

    def get_error_details(self):
        return DBConnector.instance.self.error_code, DBConnector.instance.self.error_msg

    @classmethod
    def close(cls):
        DBConnector.instance.close()

    @classmethod
    def version(cls):
        return DBConnector.instance.version()

    @classmethod
    def cursor(cls):
        return DBConnector.instance.get_cursor()

    @classmethod
    def commit(cls):
        return DBConnector.instance.commit()


def version():
    print(DBConnector.version())


def what_time():
    cur = DBConnector.cursor()
    cur.execute('select sysdate from dual')
    row = cur.fetchone()
    print(row)
    cur.close()


def binding_test():
    cur = DBConnector.cursor()
    cur.prepare('select * from IacucProtocolHeader where currentStatus= :status')
    cur.execute(None, {'status': 'ReturnToPI'})
    res = cur.fetchall()
    print(res)
    cur.execute(None, {'status': 'Approve'})
    res = cur.fetchall()
    print(res)
    cur.close()


def update():
    cur = DBConnector.cursor()
    cur.prepare("update ACT_HI_TASKINST set NAME_='Initial' where ID_ = :id")
    cur.execute(None, {'id': 'abc'})
    cur.close()
    DBConnector.commit()


def main():
    DBConnector("rascal/rascal@127.0.0.1/XE")
    version()
    what_time()
    binding_test()
    update()

if __name__ == '__main__':
    main()
