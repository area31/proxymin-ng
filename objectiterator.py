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

import string

import dbaccess
from globals import *

class ObjectIterator:
    """uniform interface to access different object types - simplifies GUI programming"""
    def __init__(self, category):
        self.dba = dbaccess.DBAccess()
        self.set_category(category)

    def set_category(self, category):
        if(category == CATEGORY_USERS or   
           category == CATEGORY_HOSTS or
           category == CATEGORY_GROUPS):
            self.category = category
        else:
            raise 'no valid category (%s)' %(category)
        
    def get_object(self, id):
        """returns according user/host/group, according to selected category"""
        if(self.category == CATEGORY_USERS):
            return self.dba.get_user(id)
        elif(self.category == CATEGORY_HOSTS):
            return self.dba.get_host(id)            
        else:
            return self.dba.get_group(id)
        
    def get_object_count(self):
        """returns number of existing user/host/group, according to selected category"""
        if(self.category == CATEGORY_USERS):
            return len(self.dba.get_user_list())
        elif(self.category == CATEGORY_HOSTS):
            return len(self.dba.get_host_list())            
        else:
            return len(self.dba.get_group_list())
        
    def get_object_id_list(self, letter=None, group=None):
        """returns list of users/hosts/groups, according to selected category\n
        'letter' can be used to restrict the returned IDs to a certain letter\n
        'group' can be used to restrict the returned IDs to members of a certain group"""        
        if(self.category == CATEGORY_USERS):
            object_list = self.dba.get_user_list()
        elif(self.category == CATEGORY_HOSTS):
            object_list = self.dba.get_host_list()
        else:
            object_list = self.dba.get_group_list()
        # restrict objects according to 'letter'/'group'
        result = []
        for id in object_list:
            if letter:
                if not (string.lower(id[0]) in letter):
                    continue
            if group:
                if group != self.get_object(id).get_group():
                    continue
            result.append(id)
        return result

    def add_object(self, id):
        if(self.category == CATEGORY_USERS):
            return self.dba.add_user(id)
        elif(self.category == CATEGORY_GROUPS):
            return self.dba.add_group(id)
        else:
            return self.dba.add_host(id)
        
    def delete_object(self, id):    
        if(self.category == CATEGORY_USERS):
            return self.dba.del_user(id)
        elif(self.category == CATEGORY_GROUPS):
            return self.dba.del_group(id)
        else:
            return self.dba.del_host(id)

    def update_object(self, object):    
        if(self.category == CATEGORY_USERS):
            return self.dba.update_user(object)
        elif(self.category == CATEGORY_GROUPS):
            return self.dba.update_group(object)
        else:
            return self.dba.update_host(object)

    def is_default_allow(self, object, protocol):
        for group_id in self.dba.get_group_list():    
            if group_id == object.get_group():
                group = self.dba.get_group(group_id)
                if protocol == PROTOCOL_FTP:
                    perm = group.get_ftp_permissions()
                else:
                    perm = group.get_http_permissions()
                default = perm.is_default_allow()
        return default           
