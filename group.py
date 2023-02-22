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

import permissions 
from globals import *
from bandwidth import Bandwidth

class Group(Bandwidth):
    """assigns permission sets and allowed file extensions to groups of users or hosts"""
    def __init__(self):
        Bandwidth.__init__(self)
        self.gid = ""
        self.description = ""
        self.httppermissions = permissions.HttpPermissions()   
        self.ftppermissions = permissions.FtpPermissions()   
        self.deniedextensions = []
    def set_gid(self, gid):
        """assign a group-ID (name of the group)"""
        self.gid = gid
    def get_gid(self):
        """get the group-ID (name of the group): same result as get_group"""
        return self.gid
    def get_group(self):
        """get the group-ID (name of the group): same result as get_gid"""
        return self.gid
    def set_description(self, description):
        """assign a description"""
        self.description = description 
    def get_description(self):
        """get the description"""
        return self.description
    def get_http_permissions(self):
        """get the permissions-object for http"""
        return self.httppermissions
    def get_ftp_permissions(self):
        """get the permissions-object for ftp"""
        return self.ftppermissions
    def deny_extension(self, extension):
        """add a file extension. Files with this extension then will be denied to be downloaded by group members"""
        self.deniedextensions.append(extension)
    def get_denied_extensions_list(self):
        """get a list of all allowed extensions"""
        return self.deniedextensions
    def is_denied_extension(self, extension):
        """returns if a given File-extension ('extension') is denied (TRUE/FALSE)"""
        for ext in self.deniedextensions:
            if ext == extension:
                return TRUE
        return FALSE
    def flush_denied_extensions(self):
        """disallow any file extension"""
        self.deniedextensions = []
    def reset(self):
        """set the group object back to initial stage. Any member variable will be reset."""
        self.gid = ""
        self.description = ""
        self.httppermissions = permissions.HttpPermissions()   
        self.ftppermissions = permissions.FtpPermissions()   
        self.allowedextensions = []
