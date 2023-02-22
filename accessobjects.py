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

import crypt
import htpasswd
from globals import *
from bandwidth import Bandwidth

class AccessObject(Bandwidth):

    def __init__(self):
        Bandwidth.__init__(self)
        self.httpurls = {}
        self.ftpurls = {}
        self.description = ""
        self.enabled = TRUE 
        # 0 = take ssl-permission from group. "NO" if not member of any grop
        # 1 = ssl always disabled 
        # 2 = ssl always enabled 
        self.ssl = 0 
        # 0 = take msn-permission from group. "NO" if not member of any grop
        # 1 = msn always disabled 
        # 2 = msn always enabled 
        self.msn = 0
        self.group = None

    def reset_http_urls(self):
        """delete any existing HTTP url"""
        self.httpurls = {}

    def reset_ftp_urls(self):
        """delete any existing FTP url"""
        self.ftpurls = {}

    def add_http_url_allowed(self, url):
        """add "url" to the list of allowed HTTP urls"""
        self.httpurls[url] = TRUE

    def add_ftp_url_allowed(self, url):
        """add "url" to the list of allowed FTP urls"""
        self.ftpurls[url] = TRUE

    def add_http_url_denied(self, url):
        """add "url" to the list of denied HTTP urls"""
        self.httpurls[url] = FALSE
 
    def add_ftp_url_denied(self, url):
        """add "url" to the list of denied FTP urls"""
        self.ftpurls[url] = FALSE
 
    def get_http_url_list(self):
        """returns a list containing any allowed or denied HTTP urls"""
        urls = self.httpurls.keys()
        urls.sort()
        return urls
    
    def get_ftp_url_list(self):
        """returns a list containing any allowed or denied FTP urls"""
        urls = self.ftpurls.keys()
        urls.sort()
        return urls

    def is_http_url_allowed(self, url):
        """returns if access to the HTTP url "url" is allowed (TRUE/FALSE)"""
        return self.httpurls[url]

    def is_ftp_url_allowed(self, url):
        """returns if access to the FTP url "url" is allowed (TRUE/FALSE)"""
        return self.ftpurls[url]

    def set_description(self, description):
        """sets the description of this object to "description" """
        self.description = description

    def get_description(self):
        """returns the description of this object"""
        return self.description

    def enable_ssl(self):
        """allows this object to access ssl protected sites"""
        self.ssl = 2

    def disable_ssl(self):
        """prohibits this object to access ssl protected sites"""
        self.ssl = 1

    def reset_ssl(self):
        """use the ssl-permissions from the group the user is member of"""
        self.ssl = 0

    def is_ssl_from_group(self):
        """Returns if access to ssl protected sites is defined by the group"""
        return self.ssl == 0

    def is_ssl_enabled(self):
        """Returns if access to ssl protected sites is always allowed, no matter what the user's group permits (TRUE/FALSE)"""
        return self.ssl == 2

    def is_ssl_disabled(self):
        """Returns if access to ssl protected sites is always prohibited, no matter what the user's group permits (TRUE/FALSE)"""
        return self.ssl == 1

    #Msn for users/hosts - Msn for groups at permissions.py
    def enable_msn(self):
        """allows this object to access msn  protected sites"""
        self.msn = 2

    def disable_msn(self):
        """prohibits this object to access msn  protected sites"""
        self.msn = 1

    def reset_msn(self):
        """use the msn -permissions from the group the user is member of"""
        self.msn = 0

    def is_msn_from_group(self):
        """Returns if access to msn protected sites is defined by the group"""
        return self.msn == 0

    def is_msn_enabled(self):
        """Returns if access to msn  protected sites is always allowed, no matter what the user's group permits (TRUE/FALSE)"""
        return self.msn == 2

    def is_msn_disabled(self):
        """Returns if access to msn  protected sites is always prohibited, no matter what the user's group permits (TRUE/FALSE)"""
        return self.msn == 1

    def set_group(self, gid):
        """sets the Group of this object to "gid" """
        # TODO: check if group really exists
        self.group = gid

    def unset_group(self):
        """cancel an existing group-membership of this object"""
        self.group = gid

    def get_group(self):
        """returns the group which this object is member of or returns "None" if the object is not member of any group"""
        return self.group

    def enable(self):
        """sets the status of this object to enabled"""
        self.enabled = TRUE

    def disable(self):
        """sets the status of this object to disabled"""
        self.enabled = FALSE
 
    def is_enabled(self):
        """returns if the status of this object is enabled (TRUE/FALSE)"""
        return self.enabled


class User(AccessObject):

    def __init__(self,uid):
        """uid is the user-ID of the newly created user"""
        AccessObject.__init__(self)
        # TODO: check if the user already exists
        self.uid = uid
        self.password = ""
        self.admin = FALSE
 
    def get_uid(self):
        """returns the user-ID of the user"""
        return self.uid

    def set_encrypted_password(self, pwd):
        """assigns the given password to the user without encrypting it"""
        self.password = pwd

    def set_password(self, pwd):
        """encrypts the given password (pwd) with crypt and assigns it to the user"""
        self.password = htpasswd.encrypt(pwd)

    def validate_password(self, pwd):
        """checks if the given password (pwd) is valid. Returns TRUE/FALSE"""
        salt = self.password[:2]
        return crypt.crypt(pwd, salt) == self.password

    def get_password(self):
        """returns the encrypted password of the user"""
        return self.password


class Host(AccessObject):

    def __init__(self,ip):
        AccessObject.__init__(self)
        self.ip = ip
 
    def get_ip(self):
        """returns the IP of the host"""
        return self.ip
