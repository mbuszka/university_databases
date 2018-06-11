import psycopg2
import os
from sys import stderr

dbg = True

def log(msg):
    if dbg:
        stderr.write("DB: {}\n".format(msg))

class Database:
    def __init__(self, dbname, user, passwd, host='localhost'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=passwd, host=host)

    def __del__(self):
        self.conn.close()

    def init_database(self):
        path = os.path.dirname(__file__)
        file = path + '/model.sql'
        crsr = self.conn.cursor()
        with open(file, 'r') as f:
            commands = f.read()
        crsr.execute(commands)
        self.conn.commit()
        crsr.close()
    
    def add_root(self, id, passwd, data):
        crsr = self.conn.cursor()
        crsr.execute(
            """
            INSERT INTO employees
            VALUES (%s, crypt(%s, gen_salt('md5')), %s, %s, NULL)
            """,
            (id, passwd, data, id))
        crsr.close()
        self.conn.commit()
        log('add root: {} {} {}'.format(id, passwd, data))

    def add_emp(self, emp, passwd, data, parent):
        crsr = self.conn.cursor()
        crsr.execute(
            "SELECT path FROM employees WHERE id=%s",
            (parent,))
        path = crsr.fetchone()[0] + ".{}".format(emp)
        crsr.execute(
            """
            INSERT INTO employees
            VALUES (%s, crypt(%s, gen_salt('md5')), %s, %s, %s)
            """,
            (emp, passwd, data, path, parent))
        self.conn.commit()
        log('add emp: {} {} {} {}'.format(emp, passwd, data, path))
    
    def auth(self, emp, passwd):
        crsr = self.conn.cursor()
        crsr.execute(
            """
            SELECT passwd = crypt(%s, passwd), path
            FROM employees
            WHERE id = %s
            """,
            (passwd, emp))
        status = crsr.fetchone()
        crsr.close()
        log('auth {} {} {}'.format(emp, passwd, status))
        return status

    def lookup(self, emp):
        crsr = self.conn.cursor()
        crsr.execute(
            "SELECT data, path, parent FROM employees WHERE id = %s",
            (emp,))
        res = crsr.fetchone()
        log('lookup {} {}'.format(emp, res))
        crsr.close()
        return res

    def remove(self, emp):
        crsr = self.conn.cursor()
        crsr.execute(
            "DELETE FROM employees WHERE id = %s",
            (emp,))
        self.conn.commit()
        crsr.close()

    def update(self, emp, data):
        crsr = self.conn.cursor()
        crsr.execute(
            """
            UPDATE employees
            SET data = %s
            WHERE id = %s
            """,
            (data, emp))
        crsr.close()
        self.conn.commit()
        log('update {} new data: {}'.format(emp, data))

    def children(self, emp):
        crsr = self.conn.cursor()
        crsr.execute(
            "SELECT id FROM employees WHERE parent = %s",
            (emp,))
        data = [emp for (emp,) in crsr.fetchall()]
        crsr.close()
        log('children of {}, cnt {}'.format(emp, len(data)))
        return data

    def ancestors(self, emp, path):
        crsr = self.conn.cursor()
        crsr.execute(
            """
            SELECT id FROM employees
            WHERE %s LIKE path || '.%%' 
            """,
            (path,))
        data = [emp for (emp,) in crsr.fetchall()]
        crsr.close()
        log('ancestors of {}, cnt {}'.format(emp, len(data)))
        return data
    
    def descendants(self, emp, path):
        crsr = self.conn.cursor()
        crsr.execute(
            """
            SELECT id FROM employees
            WHERE path LIKE %s
            """,
            (path + '.%',))
        data = [emp for (emp,) in crsr.fetchall()]
        log('descendants {} {}'.format(emp, len(data)))
        crsr.close()
        return data