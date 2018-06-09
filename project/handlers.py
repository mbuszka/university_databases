import json
from sys import stderr
from database import Database

dbg = True

def log(msg):
    if dbg:
        stderr.write("Handler: {}\n".format(msg))

def err(debug):
    return {'status': 'ERROR', 'debug': debug}

def ok(data=None):
    res = {'status': 'OK'}
    if data is not None:
        res['data'] = data
    return res

def is_ok(status):
    return status['status'] == 'OK'

def ancestor(path1, path2):
    return path2.startswith(path1) and path1 != path2

def descendant(path1, path2):
    return path1.startswith(path2) and path1 != path2

class Handler:
    def __init__(self, mode='app'):
        self.db = None
        self.mode = mode

    def open(self, dbname, user, passwd):
        try:
            self.db = Database(dbname, user, passwd)
        except:
            stderr.write('exception')
            return err('Could not connect to database')
        
        if self.mode == 'init':
            self.db.init_database()
        
        return ok()

    def root(self, emp, passwd, data):
        if self.mode != 'init':
            return err('Not in init mode')

        self.db.add_root(emp, passwd, data)
        return ok()
    
    def new(self, emp, passwd, data, parent):
        self.db.add_emp(emp, passwd, data, parent)
        return ok()

    def auth(self, admin, passwd, emp=None):
        (match, admin_path) = self.db.auth(admin, passwd)
        if not match:
            return err('Invalid password')
        log('auth {} {} {}'.format(admin, passwd, emp))
        if emp is not None:
            log('auth admin {} emp {}'.format(admin, emp))
            data, path, _ = self.db.lookup(emp)
            if not path.startswith(admin_path):
                return err('No permission')
            return ok(data)
        else:
            return ok()
    
    def children(self, emp):
        if not self.db.lookup(emp):
            return err('Not found')
        data = self.db.children(emp)
        return ok(data)

    def parent(self, emp):
        parent = self.db.lookup(emp)[2]
        return ok(parent)
    
    def ancestors(self, emp):
        path = self.db.lookup(emp)[1]
        data = self.db.ancestors(emp, path)
        return ok(data)

    def descendants(self, emp):
        path = self.db.lookup(emp)[1]
        data = self.db.descendants(emp, path)
        return ok(data)

    def remove(self, emp):
        self.db.remove(emp)
        return ok()

    def update(self, emp, data):
        self.db.update(emp, data)
        return ok()

    def handle(self, line):
        args = json.loads(line)
        cmd = list(args.keys())[0]
        data = args[cmd]

        if cmd == 'open':
            return self.open(data['database'], data['login'], data['password'])

        elif cmd == 'root':
            if data['secret'] != 'qwerty':
                return err('Invalid secret')
            return self.root(data['emp'], data['newpassword'], data['data'])

        elif cmd == 'new':
            a = self.auth(data['admin'], data['passwd'], data['emp1'])
            if not is_ok(a):
                return a
            else:
                return self.new(data['emp'], data['newpasswd'], data['data'], data['emp1'])
            
        elif cmd == 'remove':
            a = self.auth(data['admin'], data['passwd'], data['emp'])
            if not is_ok(a):
                return a
            else:
                return self.remove(data['emp'])

        elif cmd == 'update':
            log('update handler')
            a = self.auth(data['admin'], data['passwd'], data['emp'])
            if not is_ok(a):
                log('update handler no auth')
                return a
            else:
                return self.update(data['emp'], data['newdata'])

        elif cmd == 'read':
            return self.auth(data['admin'], data['passwd'], data['emp'])

        else:
            a = self.auth(data['admin'], data['passwd'])
            if not is_ok(a):
                return a
            else:
                if cmd == 'child':
                    return self.children(data['emp'])
                
                elif cmd == 'parent':
                    return self.parent(data['emp'])

                elif cmd == 'descendants':
                    return self.descendants(data['emp'])

                elif cmd == 'ancestors':
                    return self.ancestors(data['emp'])

                elif cmd == 'ancestor':
                    path1 = self.db.lookup(data['emp2'])[1]
                    path2 = self.db.lookup(data['emp1'])[1]
                    return ok(ancestor(path1, path2))

                else:
                    return err('Unknown command')

