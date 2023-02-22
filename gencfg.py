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

import string
import os

import configparser

from globals import *
import dbaccess
import permissions

config = configparser.ConfigParser()
config.add_section('files')
config.read(CONFIG_FILE_PATH + CONFIG_FILE)

# if the dbase-files do not exist they are created automatically

squid_cfg = config.get('files', 'squid_cfg')
static_cfg = config.get('files', 'static_cfg')
squid_reconfigure_command = config.get('commands',
        'squid_reconfigure_command')
case_sensitive = config.get('parameters', 'case_sensitive') == 'TRUE'


def create_acl(
    id,
    category,
    urls,
    protocol,
    permission=NONE,
    ):

    # category types
    # g = group
    # h = host
    # u = user

    if category == CATEGORY_GROUPS:
        object_string = 'g_' + id
    elif category == CATEGORY_HOSTS:
#        object_string = 'h_' + string.replace(id, '.', '_')
        object_string = 'h_' + id.replace('.', '_')
    else:
        object_string = 'u_' + id
    result = 'acl ' + object_string + '_'

    # protocol types
    # h = http
    # f = ftp

    if protocol == PROTOCOL_HTTP:
        result += 'h'

        # Nome do arquivo a ser gerado para salvar os sites

        nameoffile = config.get('files', 'squid_cfg_dir') \
            + object_string + '_h'
    else:

        # fim nome do arquivo

        result += 'f'

        # Nome do arquivo a ser gerado para salvar os sites 

        nameoffile = config.get('files', 'squid_cfg_dir') \
            + object_string + '_f'

        # fim nome do arquivo
    # permission types
    # a = allowed
    # d = denied

    if permission == ALLOWED:
        result += '_a'

        # Nome do arquivo a ser gerado para salvar os sites

        nameoffile += '_a'
    elif permission == DENIED:

        # fim nome do arquivo

        result += '_d'

        # Nome do arquivo a ser gerado para salvar os sites

        nameoffile += '_d'

        # fim nome do arquivo

    result += ' url_regex'
    if not case_sensitive:
        result += ' -i '

    # Create a file with references os urls
    # Openfile

    filehandleit = open(nameoffile, 'w')

    # Nome do arquivo para a acl do squid.conf

    result += '"' + nameoffile + '"'

    # print goit.read()

    for url in urls:

#       ....filehandleit.write('^')

        if protocol == PROTOCOL_HTTP:

        # Create a file with references os urls

            filehandleit.write('^')
            filehandleit.write('(http://.*')
            filehandleit.write(url)
            filehandleit.write('|.*')
            filehandleit.write(url)
            filehandleit.write('.*:443)\n')
        else:

            # Create a file with references os urls

            filehandleit.write('ftp://')
            filehandleit.write(url)
            filehandleit.write('\n')
    filehandleit.close()
    return result + '\n'


def is_allowed_urls_empty(object, protocol):
    if protocol == PROTOCOL_HTTP:
        urls = object.get_http_url_list()
    else:
        urls = object.get_ftp_url_list()
    for url in urls:
        if protocol == PROTOCOL_HTTP:
            if object.is_http_url_allowed(url):
                return FALSE
        else:
            if object.is_ftp_url_allowed(url):
                return FALSE
    return TRUE


def is_denied_urls_empty(object, protocol):
    if protocol == PROTOCOL_HTTP:
        urls = object.get_http_url_list()
    else:
        urls = object.get_ftp_url_list()
    for url in urls:
        if protocol == PROTOCOL_HTTP:
            if not object.is_http_url_allowed(url):
                return FALSE
        else:
            if not object.is_ftp_url_allowed(url):
                return FALSE
    return TRUE


def is_ssl_enabled(object):
    if object.is_ssl_enabled():
        return TRUE
    elif object.is_ssl_disabled():
        return FALSE
    else:
        a = dbaccess.DBAccess()
        group = a.get_group(object.get_group())
        if group.get_http_permissions().is_ssl_enabled():
            return TRUE
        else:
            return FALSE


def create_http_access(id, category):
    a = dbaccess.DBAccess()
    if category == CATEGORY_HOSTS:
        object = a.get_host(id)
#        object_string = 'h_' + string.replace(id, '.', '_')
        object_string = 'h_' + id.replace('.', '_')

    else:
        object = a.get_user(id)
        object_string = 'u_' + id
    group = a.get_group(object.get_group())
    result = ''
    if object.is_enabled():

        # denied extensions

        if len(group.get_denied_extensions_list()) > 0:
            result += 'http_access deny ' + object_string + ' g_' \
                + object.get_group() + '_e\n'

        # denied URLs for user/host

        if not is_denied_urls_empty(object, PROTOCOL_HTTP):
            result += 'http_access deny ' + object_string \
                + ' HTTP http_ports ' + object_string + '_h_d\n'
            if is_ssl_enabled(object):
                result += 'http_access deny ' + object_string \
                    + ' CONNECT SSL_ports ' + object_string + '_h_d\n'

#

        if not is_denied_urls_empty(object, PROTOCOL_FTP):
            result += 'http_access deny ' + object_string \
                + ' FTP ftp_ports ' + object_string + '_f_d\n'

        # allowed URLs for user/host

        if not is_allowed_urls_empty(object, PROTOCOL_HTTP):
            result += 'http_access allow ' + object_string \
                + ' HTTP http_ports ' + object_string + '_h_a\n'
            if is_ssl_enabled(object):
                result += 'http_access allow ' + object_string \
                    + ' CONNECT SSL_ports ' + object_string + '_h_a\n'

        if not is_allowed_urls_empty(object, PROTOCOL_FTP):
            result += 'http_access allow ' + object_string \
                + ' FTP ftp_ports ' + object_string + '_f_a\n'

        # MSN FOR USERS AND HOSTS AND Default as Group

        if object.is_msn_from_group():
            b = dbaccess.DBAccess()
            group2 = b.get_group(object.get_group())
            if group2.get_http_permissions().is_msn_enabled():
                result += 'http_access allow ' + object_string \
                    + ' CONNECT MSNICQGTALK_ports\n'
                result += 'http_access allow ' + object_string \
                    + ' MSNICQGTALK_sites\n'
                result += 'http_access allow ' + object_string \
                    + ' MSN_mime'
                result += '\n'
            else:
                result += 'http_access deny ' + object_string \
                    + ' CONNECT MSNICQGTALK_ports\n'
                result += 'http_access deny ' + object_string \
                    + ' MSNICQGTALK_sites\n'
                result += 'http_access deny ' + object_string \
                    + ' MSN_mime'
                result += '\n'
        else:
            if object.is_msn_enabled():
                result += 'http_access allow ' + object_string \
                    + ' CONNECT MSNICQGTALK_ports\n'
                result += 'http_access allow ' + object_string \
                    + ' MSNICQGTALK_sites\n'
                result += 'http_access allow ' + object_string \
                    + ' MSN_mime'
                result += '\n'
            else:
                result += 'http_access deny ' + object_string \
                    + ' CONNECT MSNICQGTALK_ports\n'
                result += 'http_access deny ' + object_string \
                    + ' MSNICQGTALK_sites\n'
                result += 'http_access deny ' + object_string \
                    + ' MSN_mime'
                result += '\n'

    # URLs for group

        if len(group.get_http_permissions().get_url_list()) > 0 \
            or group.get_http_permissions().is_default_allow():
            result += 'http_access allow ' + object_string \
                + ' HTTP http_ports'
            if len(group.get_http_permissions().get_url_list()) > 0:
                if group.get_http_permissions().is_default_allow():
                    result += ' !'
                else:
                    result += ' '
                result += 'g_' + object.get_group() + '_h'
            result += '\n'
            if is_ssl_enabled(object):
                result += 'http_access allow ' + object_string \
                    + ' CONNECT SSL_ports'
                if len(group.get_http_permissions().get_url_list()) > 0:
                    if group.get_http_permissions().is_default_allow():
                        result += ' !'
                    else:
                        result += ' '
                    result += 'g_' + object.get_group() + '_h'
                result += '\n'

#        if is_msn_enabled(object):
#               ....result += 'http_access allow ' + object_string + ' CONNECT MSN_ports\n'
# ........result += 'http_access allow ' + object_string + ' MSN_sites'
#               ....result += '\n'
#        else:
# ........result += 'http_access deny ' + object_string + ' CONNECT MSN_ports\n'
# ........result += 'http_access deny ' + object_string + ' MSN_sites '
#               ....result += '\n'

        if len(group.get_ftp_permissions().get_url_list()) > 0 \
            or group.get_ftp_permissions().is_default_allow():
            result += 'http_access allow ' + object_string \
                + ' FTP ftp_ports'
            if len(group.get_ftp_permissions().get_url_list()) > 0:
                if group.get_ftp_permissions().is_default_allow():
                    result += ' !'
                else:
                    result += ' '
                result += 'g_' + object.get_group() + '_f'
            result += '\n'
    result += 'http_access deny ' + object_string + ' all\n'
    return result


def bandwidth_limit_rule(pool, obj, bandwidth_limit=None):
    acl_definition = {'User': lambda : 'u_' + obj.get_uid(),
                      'Host': lambda : 'h_' + obj.get_ip().replace('.',
                      '_')}
    acl_name = acl_definition[obj.__class__.__name__]()

    if not bandwidth_limit:
        bandwidth_limit = obj.bandwidth_limit

    pool = str(pool)
    limit_bytes = str(int(bandwidth_limit) * 1024)
    return 'delay_class ' + pool + ' 2\n' + 'delay_parameters ' + pool \
        + ' -1/-1 ' + limit_bytes + '/' + limit_bytes + '\n' \
        + 'delay_access ' + pool + ' allow ' + acl_name


def update():
    """reads the database content and generates the squid configuration"""

    a = dbaccess.DBAccess()
    acl_users = ''
    acl_hosts = ''
    acl_group_rules = ''
    acl_user_rules = ''
    acl_host_rules = ''
    acl_bandwidth_rules = []
    http_access = ''
    acl_access = \
    'acl localnet src 0.0.0.1-0.255.255.255	# RFC 1122 "this" network (LAN)\n'
    acl_access += 'acl localnet src 10.0.0.0/8		# RFC 1918 local private network (LAN)\n'
    acl_access += 'acl localnet src 100.64.0.0/10		# RFC 6598 shared address space (CGN)\n'
    acl_access += 'acl localnet src 169.254.0.0/16 	# RFC 3927 link-local (directly plugged) machines\n'
    acl_access += 'acl localnet src 172.16.0.0/12		# RFC 1918 local private network (LAN)\n'
    acl_access += 'acl localnet src 192.168.0.0/16		# RFC 1918 local private network (LAN)\n'
    acl_access += 'acl localnet src fc00::/7       	# RFC 4193 local private network range\n'
    acl_access += 'acl localnet src fe80::/10      	# RFC 4291 link-local (directly plugged) machines\n'
    acl_access += 'acl SSL_ports port 443\n'
    acl_access += 'acl Safe_ports port 80		# http\n'
    acl_access += 'acl Safe_ports port 21		# ftp\n'
    acl_access += 'acl Safe_ports port 443		# https\n'
    acl_access += 'acl Safe_ports port 70		# gopher\n'
    acl_access += 'acl Safe_ports port 210		# wais\n'
    acl_access += 'acl Safe_ports port 1025-65535	# unregistered ports\n'
    acl_access += 'acl Safe_ports port 280		# http-mgmt\n'
    acl_access += 'acl Safe_ports port 488		# gss-http\n'
    acl_access += 'acl Safe_ports port 591		# filemaker\n'
    acl_access += 'acl Safe_ports port 777		# multiling http\n'
    # MSN rules
    acl_access += \
        'acl MSNICQGTALK_sites url_regex -i ^messenger.hotmail.com ^nexus.passport.com ^login.live.com ^gateway.messenger.hotmail.com ^login.oscar.aol.com talk.google.com .*messenger .*icq .*gtalk .*msn.com meebo.com iloveim.com ebuddy.commsn2go.com e-messenger.net imo.im messengerfx.com webmessenger.com e-messenger.com communicationtube.net msn2go.com webmessenger.com.br ebuddy.com e-buddy.com gateway.dll .microsoft.com  evsecure-crl.verisign.com crl.verisign.com mscrl.microsoft.com crl.microsoft.com\n'
    acl_access += \
        'acl MSN_mime req_mime_type -i ^application/x-msn-messenger\n'

    for group_id in a.get_group_list():
        group = a.get_group(group_id)
        urls = []
        for url in group.get_http_permissions().get_url_list():
            urls.append(url)
        if len(urls) > 0:
            acl_group_rules += create_acl(group_id, CATEGORY_GROUPS,
                    urls, PROTOCOL_HTTP)
        urls = []
        for url in group.get_ftp_permissions().get_url_list():
            urls.append(url)
        if len(urls) > 0:
            acl_group_rules += create_acl(group_id, CATEGORY_GROUPS,
                    urls, PROTOCOL_FTP)

        # acl for extensions
        # extension abbreviation = e

        if len(group.get_denied_extensions_list()) > 0:
            acl_group_rules += 'acl g_' + group_id + '_e url_regex'
            if not case_sensitive:
                acl_group_rules += ' -i'
            for extension in group.get_denied_extensions_list():
                acl_group_rules += ' ' + extension + '$'
            acl_group_rules += '\n'

    for ip in a.get_host_list():
        host = a.get_host(ip)
#        acl_hosts += 'acl h_' + string.replace(ip, '.', '_') + ' src ' \
        acl_hosts += 'acl h_' + str.replace(ip, '.', '_') + ' src ' \
            + ip + '/32\n'
        if host.is_enabled():
            urls_allowed = []
            urls_denied = []
            for url in host.get_http_url_list():
                if host.is_http_url_allowed(url):
                    urls_allowed.append(url)
                else:
                    urls_denied.append(url)
            if len(urls_denied) > 0:
                acl_host_rules += create_acl(ip, CATEGORY_HOSTS,
                        urls_denied, PROTOCOL_HTTP, DENIED)
            if len(urls_allowed) > 0:
                acl_host_rules += create_acl(ip, CATEGORY_HOSTS,
                        urls_allowed, PROTOCOL_HTTP, ALLOWED)
            urls_allowed = []
            urls_denied = []
            for url in host.get_ftp_url_list():
                if host.is_ftp_url_allowed(url):
                    urls_allowed.append(url)
                else:
                    urls_denied.append(url)
            if len(urls_denied) > 0:
                acl_host_rules += create_acl(ip, CATEGORY_HOSTS,
                        urls_denied, PROTOCOL_FTP, DENIED)
            if len(urls_allowed) > 0:
                acl_host_rules += create_acl(ip, CATEGORY_HOSTS,
                        urls_allowed, PROTOCOL_FTP, ALLOWED)
        http_access += create_http_access(ip, CATEGORY_HOSTS) + '\n'

    for uid in a.get_user_list():
        user = a.get_user(uid)
        acl_users += 'acl u_' + uid + ' proxy_auth ' + uid + '\n'
        if user.is_enabled():
            urls_allowed = []
            urls_denied = []
            for url in user.get_http_url_list():
                if user.is_http_url_allowed(url):
                    urls_allowed.append(url)
                else:
                    urls_denied.append(url)
            if len(urls_denied) > 0:
                acl_user_rules += create_acl(uid, CATEGORY_USERS,
                        urls_denied, PROTOCOL_HTTP, DENIED)
            if len(urls_allowed) > 0:
                acl_user_rules += create_acl(uid, CATEGORY_USERS,
                        urls_allowed, PROTOCOL_HTTP, ALLOWED)
            urls_allowed = []
            urls_denied = []
            for url in user.get_ftp_url_list():
                if user.is_ftp_url_allowed(url):
                    urls_allowed.append(url)
                else:
                    urls_denied.append(url)
            if len(urls_denied) > 0:
                acl_user_rules += create_acl(uid, CATEGORY_USERS,
                        urls_denied, PROTOCOL_FTP, DENIED)
            if len(urls_allowed) > 0:
                acl_user_rules += create_acl(uid, CATEGORY_USERS,
                        urls_allowed, PROTOCOL_FTP, ALLOWED)

        http_access += create_http_access(uid, CATEGORY_USERS) + '\n'

    # Bandwidth limit

    acl_bandwidth_pools = 0
    for uid in a.get_user_list():
        user = a.get_user(uid)
        if not user.is_bandwidth_limit_disabled():
            acl_bandwidth_pools += 1
            acl_bandwidth_rules.append(bandwidth_limit_rule(acl_bandwidth_pools,
                    user))

    for ip in a.get_host_list():
        host = a.get_host(ip)
        if not host.is_bandwidth_limit_disabled():
            acl_bandwidth_pools += 1
            acl_bandwidth_rules.append(bandwidth_limit_rule(acl_bandwidth_pools,
                    host))

    for gid in a.get_group_list():
        group = a.get_group(gid)
        if not group.is_bandwidth_limit_disabled():
            for uid in a.get_group_member_users(gid):
                user = a.get_user(uid)
                if user.is_bandwidth_limit_disabled():
                    acl_bandwidth_pools += 1
                    acl_bandwidth_rules.append(bandwidth_limit_rule(acl_bandwidth_pools,
                            user, group.bandwidth_limit))
            for ip in a.get_group_member_hosts(gid):
                host = a.get_host(ip)
                if host.is_bandwidth_limit_disabled():
                    acl_bandwidth_pools += 1
                    acl_bandwidth_rules.append(bandwidth_limit_rule(acl_bandwidth_pools,
                            host, group.bandwidth_limit))

    cfg_file = open(squid_cfg, 'w')
    static_file = open(static_cfg, 'r')

    cfg = static_file.readlines()
    cfg += '\n'
    cfg += acl_access + '\n'
    if acl_users != '':
        cfg += '''#
# users
#
'''
        cfg += acl_users + '\n'
    if acl_hosts != '':
        cfg += '''#
# hosts
#
'''
        cfg += acl_hosts + '\n'
    if acl_group_rules != '':
        cfg += '''#
# group rules
#
'''
        cfg += acl_group_rules + '\n'
    if acl_host_rules != '':
        cfg += '''#
# host rules
#
'''
        cfg += acl_host_rules + '\n'
    if acl_user_rules != '':
        cfg += '''#
# user rules
#
'''
        cfg += acl_user_rules + '\n'
    if len(acl_bandwidth_rules):
        cfg += '''#
# bandwidth limit rules
#
'''
        cfg += 'delay_pools ' + str(acl_bandwidth_pools) + '\n'
        cfg += '\n'.join(acl_bandwidth_rules) + '''

'''
    cfg += '''#
# access rules
#
'''
    cfg += http_access

    # cfg += 'http_access allow group_Padrao_http AuthenticatedUsers \n'

    cfg += 'http_access allow localnet\nhttp_access allow localhost\n# Squid normally listens to port 3128\nhttp_port 3128\nhttp_access deny all\n'
    cfg += 'coredump_dir /var/cache/squid\n'
    cfg += 'refresh_pattern ^ftp:           1440    20%     10080\n'
    cfg += 'refresh_pattern ^gopher:        1440    0%      1440\n'
    cfg += 'refresh_pattern -i (/cgi-bin/|\?) 0     0%      0\n'
    cfg += 'refresh_pattern .               0       20%     4320\n'

    cfg_file.writelines(cfg)
    cfg_file.close()
    static_file.close()
    os.system(squid_reconfigure_command)

