#proxymin - A Web-based administration frontend for the Squid Web proxy cache
#Copyright (C) 2004  Mirjam Kuhlmann (proxymin@mikuhl.de)
#Copyright (C) 2004  Clemens Hermann (proxymin@clhe.de)
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import configparser
import shelve
import pickle
import bsddb3
import accessobjects
import gencfg
import group
import htpasswd
from globals import *

# first read the configuration file
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH + CONFIG_FILE)

# if the dbase-files do not exist they are created automatically
userdb = config.get("files","db_dir") + "/users"
hostdb = config.get("files","db_dir") + "/hosts"
groupdb = config.get("files","db_dir") + "/groups"

class DBAccess:
    """persistence framework"""
    def __init__(self):
        self.users = shelve.Shelf(bsddb3.btopen(userdb, 'c'))
        self.hosts = shelve.Shelf(bsddb3.btopen(hostdb, 'c'))
        self.groups = shelve.Shelf(bsddb3.btopen(groupdb, 'c'))

    def get_host_list(self):
        """get a list of all existing hosts\n
        returns a list that contains any existing host IP\n
        returns an empty list if no host exists"""
        hosts = list(self.hosts.keys())
        hosts = sorted(hosts)
        return hosts
 
    def get_host(self, ip):
        """get the host object associated with "ip"\n
        returns the according host-object if a host with the given IP exists\n
        returns False otherwise"""
#        if self.hosts.has_key(ip):
        if ip in self.hosts:
            return self.hosts[ip]
        # returns False in case host does not exist
        return False

    def add_host(self, ip):
        """create a new host object with IP="ip" within the host database\n
        returns True if host successfully created\n
        returns False if the host did already exist"""
        if ip not in self.get_host_list():
            newhost = accessobjects.Host(ip)
            self.hosts[ip] = newhost
            return True
        # notify the caller in case the host did already exist
        return False

    def del_host(self, ip):
        """delete the host object with IP="ip" from the host database\n
        returns True if host successfully deleted\n
        returns False if the host did not exist"""
        if ip in self.get_host_list():
            del self.hosts[ip]
            # the close is needed to flush the shelve to disk
            self.hosts.close()
            gencfg.update()
            return True
        # notify the caller in case the host did not exist
        return False

    def update_host(self, host):
        """update the given host object within the host database\n
        returns True if host successfully updated\n
        returns False if the host did not exist"""
        if host.get_ip() in self.get_host_list():
            self.hosts[host.get_ip()] = host
            # the close is needed to flush the shelve to disk
            self.hosts.close()
            gencfg.update()
            return True
        # TODO: notify the caller in case the host did not exists
        return False
 
    def get_user_list(self):
        """get a list of all existing users\n
        returns a list that contains any existing user-ID\n
        returns an empty list if no users exists"""
        users = list(self.users.keys())
        users = sorted(users)
        return users

    def get_user(self, uid):
        """get the user object associated with "uid"\n
        returns the according user-object if a user with the given uid exists\n
        returns False otherwise"""
#        if self.users.has_key(uid):
        if uid in self.users:
            return self.users[uid]
        # return False if uid does not exist 
        return False

    def add_user(self, uid):
        """create a new user object with UID="uid" within the user database\n
        returns True if user successfully created\n
        returns False if the user did already exist"""
        if uid not in self.get_user_list():
            newuser = accessobjects.User(uid)
            self.users[uid] = newuser
            return True 
        # notify the caller in case the uid already exists
        return False

    def del_user(self, uid):
        """delete the user object with UID="uid" from the user database\n
        returns True if user successfully deleted\n
        returns False if the user did not exist"""
        if uid in self.get_user_list():
            del self.users[uid]
            # the close is needed to flush the shelve to disk
            self.users.close()
            htpasswd.delUser(uid)
            gencfg.update()
            return True
        # notify the caller in case the uid did not exist
        return False

    def update_user(self, user):
        """update the given user object within the user database\n
        returns True if user successfully updated\n
        returns False if the user did not exist"""
        if user.get_uid() in self.get_user_list():
            self.users[user.get_uid()] = user
            # the close is needed to flush the shelve to disk
            self.users.close()
            htpasswd.updateUser(user.get_uid(), user.get_password()) 
            gencfg.update()
            return True 
        # notify the caller in case the user did not exists
        return False

    def get_group_list(self):
        """get a list of all existing groups\n
        returns a list that contains any existing group-ID\n
        returns an empty list if no groups exists"""
        groups = list(self.groups.keys())
        groups = sorted(groups)
        return groups
 
    def get_group(self, gid):
        """get the group object associated with "gid"\n
        returns the according group-object if a group with the given gid exists\n
        returns False otherwise"""
#        if self.groups.has_key(gid):
        if gid in self.groups:
#            return pickle.loads(self.groups[gid])
            return self.groups[gid]
        # notify the caller if gid does not exist 
        return False

    def add_group(self, gid):
        """create a new group object with GID="gid" within the group database\n
        returns True if group successfully created\n
        returns False if the group did already exist"""
        if gid not in self.get_group_list():
            newgroup = group.Group()
            newgroup.set_gid(gid)
#            self.groups[gid.encode()] = pickle.dumps(newgroup)
            self.groups[gid] = newgroup
            return True
        # notify the caller in case the gid already exists
        return False

    def del_group(self, gid):
        """delete the group object with GID="gid" from the group database\n
        returns True if group successfully deleted\n
        returns False if the group did not exist\n
        returns False if the group is not empty, means: there \
        exist users which are members of this group (group will \
        not be deleted then) """
        # only delete groups without members
        # we provide our own ACID here :)
        if self.get_group_member_users(gid) != []:
            return False 
        if self.get_group_member_hosts(gid) != []:
            return False 
        if gid in self.get_group_list():
            del self.groups[gid]
            # the close is needed to flush the shelve to disk
            self.groups.close()
            gencfg.update()
            return True
        # notify the caller in case the gid did not exist
        return False

    def update_group(self, group):
        """update the given group object within the group database\n
        returns True if group successfully updated\n
        returns False if the group did not exist"""
        if group.get_gid() in self.get_group_list():
            self.groups[group.get_gid()] = group
            # the close is needed to flush the shelve to disk
            self.groups.close()
            gencfg.update()
            return True
        # notify the caller in case the group did not exists
        return False

    def get_group_member_users(self, gid):
        """get a list of all UIDs of the memners of this group\n
        returns a list that contains any existing member-UID\n
        returns an empty list if this group has no members"""
        members = []
        for uid in self.get_user_list():
            user = self.get_user(uid)
            if user.get_group() == gid:
                members.append(uid)
        members.sort()
        return members

    def get_group_member_hosts(self, gid):
        """get a list of all UIDs of the memners of this group\n
        returns a list that contains any existing member-UID\n
        returns an empty list if this group has no members"""
        members = []
        for ip in self.get_host_list():
            host = self.get_host(ip)
            if host.get_group() == gid:
                members.append(ip)
        members.sort()
        return members
