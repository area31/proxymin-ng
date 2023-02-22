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

def print_help_page():
    """show http/ftp details of an object"""
    gui_misc.print_html_head(_('Help'))
    values = {'program_name':PROGRAM_NAME,
              'help':_('Help'),
              'close':_('close'),
              'squid_homepage':SQUID_HOMEPAGE,
              'squid_acl_url':SQUID_ACL_URL,
              'gpl_url':GPL_URL,
              'project_homepage':PROJECT_HOMEPAGE,
              'python_homepage':PYTHON_HOMEPAGE,
              'contact_email':CONTACT_EMAIL,
              'config_file':CONFIG_FILE
             }
    template = """
<body>
<table cellpadding=10 cellspacing=0 border=0 width="100%%">
  <tr class="titlebar">
    <td class="title">%(program_name)s - %(help)s</td>
    <td class="links"><nobr>
      [ <a href="javascript:opener.focus();self.close();">%(close)s</a> ]
    </td>
<tr><td>
<br>
<ul>
<li><b>Configuration:</b><br>
    The main page is devided into three part: <i>groups</i>, <i>users</i> and <i>hosts</i>. The first thing you should do is to create a group.</li>
    <ul>
    <li><b>Groups:</b></li>
        <ul>
        <li>create new group:</li>
            <ul>
            <li><b>Group-ID:</b> a unique name for the group</li>
            <li><b>Description:</b> a meaningful one line description for the group (optional)</li>
            </ul>
        <li>Details:</li>
            <ul>
            <li>adjust the group description</li>
            </ul>
        <li>HTTP/FTP (configure HTTP/FTP permissions):</li>
            <ul>
            <li><b>Default:</b> allowed or denied. If the default is allowed, any HTTP/FTP url can be
               accessed by members of this group. You can deny URLs selectively
               for the whole group (see URL(1), URL(2), ...) or for individual users.
               If the default is denied it works the other way round.</li>
            <li><b>URL(1), URL(2), ...:</b> the URLs that overwrite the default (allowed or denied).
                                            if the default is allowed then these URLs are denied and
                                            vice versa. Be careful when changing the default. Then the
                                            semantics of the URLs changes.
                                            Important: do not specify the protocol in the URL again:<br>
                                            <i>right:</i> www.something.com<br>
                                            <i>wrong:</i> http://www.something.com</li>
            <li><b>SSL (HTTP only):</b> defines if https (ssl encrypted) sites can be accessed</li>
                                    <ul>
                                    <li>for SSL the same rules as for http are applied</li>
                                    <li><b>NOTE:</b> https requests can only be filtered based on domain names/IPs. The reason 
                                                     for this is that the proxy just can see nothing but the host name/IP 
                                                     of the request (e.g. www.google.com).
                                                     So the rule www\.google\.de/search* would hit the request<br> 
                                                     http://www.google.com/search?q=proxymin<br>
                                                     but it would NOT hit the request<br>
                                                     https://www.google.com/search?q=proxymin<br>
                                                     Furthermore denied file types (extensions) can be downloaded via https.
                                                     The "problem" is protocol immanent as SSL not just encrypts the single 
                                                     pages but the whole communication between browser and web server. So the 
                                                     proxy just sees the target server (hence the host name), connects to it and 
                                                     forwards the bits in both directions (that includes the actual site request). 
                                                     The proxy does no longer see the complete page-/file- etc. request and thus 
                                                     can not filter the complete requests.</li>
                                    </ul>
            </ul>            
        <li>Extensions: files with these extensions can not be accessed by members of the
                               group (you can deny the download of e.g. exe and zip files)</li>
        <li>delete: delete the group. At least one group must be left over and only groups
                           that have no members can be deleted.</li>
        </ul>
    <li><b>Users:</b>
        <ul>
        <li>create new user:</li>
            <ul>
            <li><b>User-ID:</b> a unique name for the user</li>
            <li><b>Description:</b> a meaningful one line description for the user (optional)</li>
            <li><b>Group:</b> select the group which the user belongs to. The permissions of this
                              group are applied to the user and can be partially overwritten</li>
            <li><b>Password:</b> the password the user must enter before he/she can access websites</li>
            <li><b>active:</b> enable/disable the user. A disabled user can not access the internet</li>
            </ul>
        <li>Details:</li>
            <ul>
            <li>adjust the overall parameters of the user</li>
            </ul>
        <li>HTTP/FTP (configure HTTP/FTP permissions):</li>
            <ul>
            <li><b>URL(1), URL(2), ...:</b> the URLs that overwrite the groups default (allowed or denied)
                                            Important: do not specify the protocol in the URL again:<br>
                                            <i>right:</i> www.something.com<br>
                                            <i>wrong:</i> http://www.something.com</li>
            <li><b>SSL (HTTP only):</b> defines if ssl is allowed for the user.  To retreive this parameter
                                        from the group default use "as group"</li>
            </ul>
            <li>delete: delete the user</li>
        </ul>
    <li><b>Hosts:</b>
        <ul>
        <li>create new host:</li>
        <ul>
            <li><b>IP-Address:</b> the IP-Address of the host</li>
            <li><b>Description:</b> a meaningful one line description for the host (optional)</li>
            <li><b>Group:</b> select the group which the host belongs to. The permissions of this
                              group are applied to the host and can be partially overwritten
            <li><b>active:</b> enable/disable the host. A disabled host can not access the internet
        </ul>
        <li>Details:</li>
            <ul>
            <li>adjust the overall parameters of the host</li>
            </ul>
        <li>HTTP/FTP (configure HTTP/FTP permissions):</li>
            <ul>
            <li>analogous to user</li>
            </ul>
        </ul>
    </ul>
<hr>
<li><b>Rule precedence:</b></li>
    <ul>
    <li>Group permissions vs. User/Host permissions</li>
        <ul>
        <li>the main permissions for all members should be configured in the group section</li>
        <li>if you want to deny specific types of files this is only possible via group rules (extensions)</li>
        <li>to make exceptions to the group rules for users or hosts just configure the http/ftp permission
            for the specific user/host.</li>
        <li>user/host rules overwrite the group permissions the user/host belongs to. E.g. if the group
            denies access to www.google.com and a member of this group has this url configured as allowed
            then this member can access www.google.com even if the group rules deny the access.</li>
        </ul>
    <li>Users/Hosts:</li>
        <ul>
        <li>if a host is configured, then no login window is displayed and the host/group permissions apply</li>
        <li>if a requesting host is not configured a login window (user/password) is displayed.</li>
        <li>permissions for hosts are especially useful for serves, e.g. to update the virus scanner 
            database via the proxy without having the server to do some kind of proxy login.</li>
        </ul>
    </ul>
<hr>
<li><b>Permissions:</b></li>
    <ul>
    <li>the URLs, file extensions, etc. are interpreted as regular expressions. So if you allow the url 
    go.nothing.com this will fit "go.nothing.com" but as "." is a wildcard for any letter also 
    gotnothing.com will fit. For an Intro to regular expressions have a look at one of the 
    following URLs:
        <ul>
        <li><a href="http://www.newbie.org/gazette/xxaxx/xprmnt02.html" target="_new">
            http://www.newbie.org/gazette/xxaxx/xprmnt02.html</a></li>
        <li><a href="http://jmason.org/software/sitescooper/tao_regexps.html" target="_new">
            http://jmason.org/software/sitescooper/tao_regexps.html</a></li>
        </ul>
    <li>a few examples how to use regular expressions to match URLs:
        <ul>
        <li>match www.python.org: www\.python\.org</li>
        <li>match any subdomain of python.org (info.python.org, news.python.org, www.python.org etc.): .*\.python\.org</li>
        <li>match www.python.org and news.python.org: (www|news)\.python\.org</li>
        <li>match any URL that starts with "www.": www\..*</li>
        <li>match any URL in the ".org" domain: .*\.org(/.*)?</li>
        <li>match www.python.com and www.python.org and www.python.net: www\.python\.(com|org|net)</li>
        </ul>
    </ul>
<hr>
<li><b>Internationalization:</b></li>
    <ul>
    <li>Supported languages: Deutsch, English</li>
    <li>the language can be selected in %(config_file)s</li>
    <li>it is easy to add more languages. Just open the file lang/lang_de as template. Try to avoid
        using an already translated file as template as translation errors might be propagated. 
        Each line contains one expression in the form 'english original'::'translation'. Translate 
        each line  so that the translation (the string after "::") corresponds to the english 
        original string in your language.
        The first lines should tell which language the file matches and your name and email-addresse
        so you can be contacted in case new expressions are added.
        Now save the file in the "lang" directory as "lang_countrycode" where "countycode" is the code
        of your language (en for english, de for german, fr for french etc.).
        Adjust the language parameter in %(config_file)s and try it out.
        Now please do not forget to email the file to <a href="mailto:%(contact_email)s">%(contact_email)s</a>
        so your language file can be included into the official distribution.</li>
    </ul>
<hr>
</ul>
<center>for your suggestions, requests and bugfixes please send an email to
        <a href="mailto:%(contact_email)s">%(contact_email)s</a></center>
<br>
"""
    print template % values

    gui_misc.print_footer()
