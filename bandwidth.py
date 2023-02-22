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

class Bandwidth:
    def __init__(self):
        self.bandwidth_limit = ''

    def __setstate__(self, state):
        if 'bandwidth_limit' not in state:
            Bandwidth.__init__(self)
        self.__dict__.update(state)

    def is_bandwidth_limit_disabled(self):
        return not self.bandwidth_limit
    
    def set_bandwidth_limit(self, limit):
        self.bandwidth_limit = limit
