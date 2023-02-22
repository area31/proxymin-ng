import sqlite3
import os

class DBAccess:
    def __init__(self, userdb='db/users.db', groupdb='db/groups.db', hostdb='db/hosts.db'):
        if not os.path.exists(userdb):
            sqlite3.connect(userdb).close()
        if not os.path.exists(groupdb):
            sqlite3.connect(groupdb).close()
        if not os.path.exists(hostdb):
            sqlite3.connect(hostdb).close()

        self.conn = sqlite3.connect('file:' + userdb + '?mode=rw', uri=True)
        self.users = self.conn.cursor()
        self.users.execute('''CREATE TABLE IF NOT EXISTS users (name text primary key, password text, groupname text)''')
        self.users.execute('''CREATE INDEX IF NOT EXISTS idx_users_groupname ON users (groupname)''')

        self.conn = sqlite3.connect('file:' + groupdb + '?mode=rw', uri=True)
        self.groups = self.conn.cursor()
        self.groups.execute('''CREATE TABLE IF NOT EXISTS groups (name text primary key)''')

        self.conn = sqlite3.connect('file:' + hostdb + '?mode=rw', uri=True)
        self.hosts = self.conn.cursor()
        self.hosts.execute('''CREATE TABLE IF NOT EXISTS hosts (name text primary key, ip text, domain text, groupname text, description text)''')

    def __del__(self):
        self.conn.close()

    def get_user(self, name):
        self.users.execute("SELECT * FROM users WHERE name = ?", (name,))
        row = self.users.fetchone()
        if row is not None:
            name, password, groupname = row
            return (name, password, groupname)
        else:
            return None

    def put_user(self, name, password, groupname):
        try:
            self.users.execute("INSERT INTO users VALUES (?, ?, ?)", (name, password, groupname))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def del_user(self, name):
        self.users.execute("DELETE FROM users WHERE name = ?", (name,))
        self.conn.commit()

    def get_users(self):
        self.users.execute("SELECT * FROM users")
        rows = self.users.fetchall()
        users = []
        for row in rows:
            name, password, groupname = row
            users.append((name, password, groupname))
        return users

    def get_users_in_group(self, groupname):
        self.users.execute("SELECT * FROM users WHERE groupname = ?", (groupname,))
        rows = self.users.fetchall()
        users = []
        for row in rows:
            name, password, groupname = row
            users.append((name, password, groupname))
        return users

    def get_group(self, name):
        self.groups.execute("SELECT * FROM groups WHERE name = ?", (name,))
        row = self.groups.fetchone()
        if row is not None:
            name, = row
            return name
        else:
            return None

    def put_group(self, name):
        try:
            self.groups.execute("INSERT INTO groups VALUES (?)", (name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def del_group(self, name):
        self.groups.execute("DELETE FROM groups WHERE name = ?", (name,))
        self.conn.commit()

    def get_groups(self):
        self.groups.execute("SELECT * FROM groups")
        rows = self.groups.fetchall()
        groups = []
        for row in rows:
            name, = row
            groups.append(name)
        return groups

    def get_host(self, name):
        host = None
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM hosts WHERE name=?", (name,))
            row = c.fetchone()
            if row:
                host = Host(row[0])
                host.parse_db_row(row)
        except:
            traceback.print_exc()
        return host

    def get_user(self, name):
        user = None
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM users WHERE name=?", (name,))
            row = c.fetchone()
            if row:
                user = User(row[0])
                user.parse_db_row(row)
        except:
            traceback.print_exc()
        return user

    def get_group(self, name):
        group = None
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM groups WHERE name=?", (name,))
            row = c.fetchone()
            if row:
                group = Group(row[0])
                group.parse_db_row(row)
        except:
            traceback.print_exc()
        return group

    def remove_host(self, hostname):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM hosts WHERE name=?", (hostname,))
            self.conn.commit()
        except:
            traceback.print_exc()

    def remove_user(self, username):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM users WHERE name=?", (username,))
            self.conn.commit()
        except:
            traceback.print_exc()

    def remove_group(self, groupname):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM groups WHERE name=?", (groupname,))
            self.conn.commit()
        except:
            traceback.print_exc()

    def add_host(self, host):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO hosts(name, ip, domain) VALUES (?,?,?)", (host.name, host.ip, host.domain))
            self.conn.commit()
        except:
            traceback.print_exc()

    def add_user(self, user):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO users(name, passwd, groups) VALUES (?,?,?)", (user.name, user.passwd, ';'.join(user.groups)))
            self.conn.commit()
        except:
            traceback.print_exc()

    def add_group(self, group):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO groups(name, members) VALUES (?,?)", (group.name, ';'.join(group.members)))
            self.conn.commit()
        except:
            traceback.print_exc()

    def update_host(self, host):
        try:
            c = self.conn.cursor()
            c.execute("UPDATE hosts SET ip=?, domain=? WHERE name=?", (host.ip, host.domain, host.name))
            self.conn.commit()
        except:
            traceback.print_exc()

    def update_user(self, user):
        try:
            c = self.conn.cursor()
            c.execute("UPDATE users SET passwd=?, groups=? WHERE name=?", (user.passwd, ';'.join(user.groups), user.name))
            self.conn.commit()
        except:
            traceback.print_exc()

    def update_group(self, group):
        try:
            c = self.conn.cursor()
            c.execute("UPDATE groups SET members=? WHERE name=?", (';'.join(group.members), group.name))
            self.conn.commit()
        except:
            traceback.print_exc()

    def get_host_list(self):
        self.hosts.execute("SELECT name, ip, groupname, description FROM hosts")
        return self.hosts.fetchall()
    
    def get_user_list(self):
        self.hosts.execute("SELECT name, ip, groupname, description FROM hosts")
        return self.hosts.fetchall()
    
    def get_group_list(self):
        self.hosts.execute("SELECT name, ip, groupname, description FROM hosts")
        return self.hosts.fetchall()
    
