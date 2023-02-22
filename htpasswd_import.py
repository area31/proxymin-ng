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

import dbaccess

#set this to the path where your hapache password file can be found
PASSWD_SOURCE = '/tmp/passwd'
#set this to an existing group.
# All imported users will initially be member of this group
GROUP = 'user'

myfile = open(PASSWD_SOURCE, "r")

for line in myfile.readlines()[0:-1]:
    a = dbaccess.DBAccess()
    uid = line.split(":")[0]
    password = line.split(":")[1][:-1]
    print uid
    a.add_user(uid)
    user = a.get_user(uid)
    user.set_encrypted_password(password)
    user.set_group(GROUP)
    a.update_user(user)

myfile.close()
