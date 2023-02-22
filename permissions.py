# -*- coding: utf-8 -*-
# proxymin - A Web-based administration frontend for the Squid Web proxy cache
# Copyright (C) 2004  Mirjam Kuhlmann (proxymin@mikuhl.de)
# Copyright (C) 2004  Clemens Hermann (proxymin@clhe.de)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from globals import *
from bandwidth import Bandwidth


class Permissions:

    def __init__(self):
        self.allow = FALSE
        self.urls = []

    def set_default_allow(self):
        """any URL is allowed, as long as it is not listed from get_url_list"""

        self.allow = TRUE

    def set_default_deny(self):
        """any URL is denied, as long as it is not listed from get_url_list"""

        self.allow = FALSE

    def is_default_allow(self):
        """returns TRUE if default is allow. Returns FALSE otherwise"""

        return self.allow

    def add_url(self, url):
        """add "url to the list of allowed/denied URLs. The effect of this depends to if set_default_allow() or set_default_deny() has been set"""

        # TODO: it might be useful to notify the caller in case "url" already exists

        if url not in self.urls:
            self.urls.append(url)
            self.urls.sort()

    def flush_urls(self):
        """delete any url from the url list. If the default is to allow any, this call enables unlimited access. If the default is to deny, this call disables anything"""

        self.urls = []

    def is_unrestricted(self):
        """returns if access is unrestricted (TRUE/FALSE)"""

        return self.allow == TRUE and len(self.urls) == 0

    def is_restricted(self):
        """returns if access is restricted (TRUE/FALSE)"""

        return len(self.urls) != 0

    def is_disabled(self):
        """returns if access is disabled (TRUE/FALSE)"""

        return self.allow == FALSE and len(self.urls) == 0

    def get_url_list(self):
        '''returns the list of URLs. Depending to if set_default_allow() or set_default_deny() has been set these urls are allowed or denied'''

        return self.urls

    def reset(self):
        """resets any member varianble to its initial stage"""

        self.allow = FALSE
        self.urls = []


class HttpPermissions(Permissions):

    def __init__(self):
        Permissions.__init__(self)
        self.ssl = FALSE
        self.msn = FALSE

    def enable_ssl(self):
        """allows ssl connections"""

        self.ssl = TRUE

    def disable_ssl(self):
        """permits ssl connections"""

        self.ssl = FALSE

    def is_ssl_enabled(self):
        """returns if ssl connections are allowed (TRUE/FALSE)"""

        return self.ssl

    # Msn for groups - for users/hosts check at accessobjects.py

    def enable_msn(self):
        """allows msn connections"""

        self.msn = TRUE

    def disable_msn(self):
        """permits msn connections"""

        self.msn = FALSE

    def is_msn_enabled(self):
        """returns if msn connections are allowed (TRUE/FALSE)"""

        return self.msn

    def reset(self):
        """resets any member varianble to its initial stage"""

        Permissions.reset(self)
        self.ssl = False
        self.msn = FALSE


class FtpPermissions(Permissions):

    def __init__(self):
        Permissions.__init__(self)

