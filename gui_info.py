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

import gui_misc
from globals import *
from localization import _

def print_info_page():
    """show http/ftp details of an object"""
    gui_misc.print_html_head(_('Info'))
    values = {'program_name':PROGRAM_NAME,
              'info':_('Info'),
              'close':_('close'),
              'squid_homepage':SQUID_HOMEPAGE,
              'squid_acl_url':SQUID_ACL_URL,
              'gpl_url':GPL_URL,
              'project_homepage':PROJECT_HOMEPAGE,
              'python_homepage':PYTHON_HOMEPAGE,
              'contact_email':CONTACT_EMAIL
             }
    template = """
<body>
<table cellpadding=10 cellspacing=0 border=0 width="100%%">
  <tr class="titlebar">
    <td class="title">%(program_name)s - %(info)s</td>
    <td class="links"><nobr>
      [ <a href="javascript:opener.focus();self.close();">%(close)s</a> ]
    </td>


<tr><td>
<br>
<ul>
<li>%(program_name)s is a Web-based administration frontend for the <a href="%(squid_homepage)s" target="_new">Squid </a> Web proxy cache<br>
<br></li>

<li>Features:
<ul>
<li>easy to use graphical interface to configure commonly needed <a href="%(squid_acl_url)s" target="_new">Squid ACLs</a></li>
<li>fine-grained permission management based on users/hosts/groups</li>
<li>create/edit/delete/enable/disable users and hosts</li>
<li>Protocols HTTP/HTTPS/FTP are currently supported</li>
<li>multi language support</li>
<li>user authentication based on standard NCSA auth</li>
<li>tested with several hundreds of managed accounts</li>
<li>self-contained database and policy compiler for easy porting to alternative proxys</li>
</ul>
<br></li>
                 
<li>This software is copyright and maintained by Mirjam Kuhlmann and Clemens Hermann. <br>
It is licensed under the terms of the <a href="%(gpl_url)s" target="_new">GPL</a><br><br></li>
         
<li>Supported languages:<font color="blue">Brazilian Portuguese, Deutsch, English</font><br>
if you want to see your language here then just use the file lang/lang_de as template
<br>and adapt it to fit your language</li><br><br>   

<li>%(program_name)s is programmed in <a href="%(python_homepage)s" target="_new">python</a><br><br></li>

<li>For more information on %(program_name)s visit the <a href="%(project_homepage)s" target="_new">project homepage</a>
</li>
<br><br>
<li>
for your suggestions, requests and bugfixes please send an email to <a href="mailto:%(contact_email)s">%(contact_email)s</a><br>
</li>
</ul></td></tr>
</table>

</td></tr></table>
<br>
"""
    print template % values

    gui_misc.print_footer()
