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

import cgi
import os
import string
import sys

import configparser

import dbaccess
import gui_misc
import objectiterator
from globals import *
from localization import _


def print_details_page(category, action, id):
    """show http/ftp details of an object"""

    if action == ACTION_EDIT_HTTP_PERMISSIONS:
        title = _('HTTP - modify permissions')
    elif action == ACTION_EDIT_FTP_PERMISSIONS:
        title = _('FTP - modify permissions')
    else:
        raise 'no valid action (%s)' % action

    if category == CATEGORY_USERS or category == CATEGORY_HOSTS:
        colspan = 4
    else:
        colspan = 2

    gui_misc.print_popup_head(colspan, title)

    iterator = objectiterator.ObjectIterator(category)
    object = iterator.get_object(id)
    if category == CATEGORY_USERS or category == CATEGORY_HOSTS:
        group = object.get_group()
    else:
        group = ''

    print_details_form(category, action, id, group)


def print_confirmation_page(
    category,
    id,
    action,
    group='',
    ):
    """confirm successful changes"""

    title = _('changes saved')

    if category == CATEGORY_USERS or category == CATEGORY_HOSTS:
        colspan = 4
    else:
        colspan = 2

    gui_misc.print_popup_head(colspan, title)
    print_details_form(category, action, id, group)


def save_input_data(
    category,
    id,
    action,
    url_list,
    url_status_list,
    ssl,
    default,
    ):
    iterator = objectiterator.ObjectIterator(category)
    object = iterator.get_object(id)
    if category == CATEGORY_GROUPS:
        if default == ALLOWED:
            if action == ACTION_SAVE_HTTP_PERMISSIONS:
                object.get_http_permissions().set_default_allow()
            else:
                object.get_ftp_permissions().set_default_allow()
        else:
            if action == ACTION_SAVE_HTTP_PERMISSIONS:
                object.get_http_permissions().set_default_deny()
            else:
                object.get_ftp_permissions().set_default_deny()
        if action == ACTION_SAVE_HTTP_PERMISSIONS:
            if ssl == SSL_ENABLED:
                object.get_http_permissions().enable_ssl()
            else:
                object.get_http_permissions().disable_ssl()

# ....    if(msn == MSN_ENABLED):
#                object.get_http_permissions().enable_msn()
#            else:
#                object.get_http_permissions().disable_msn()

            object.get_http_permissions().flush_urls()
            for url in url_list:
                object.get_http_permissions().add_url(url)
        else:
            object.get_ftp_permissions().flush_urls()
            for url in url_list:
                object.get_ftp_permissions().add_url(url)
    else:
        if action == ACTION_SAVE_HTTP_PERMISSIONS:
            if ssl == SSL_ENABLED:
                object.enable_ssl()
            elif ssl == SSL_DISABLED:
                object.disable_ssl()
            else:
                object.reset_ssl()

# ....    if(msn == MSN_ENABLED):
#                object.enable_msn()
#            elif(msn == MSN_DISABLED):
#                object.disable_msn()
#            else:
#                object.reset_msn()

            object.reset_http_urls()
            for i in range(len(url_list)):
                if url_status_list[i] == 'allowed':
                    object.add_http_url_allowed(url_list[i])
                else:
                    object.add_http_url_denied(url_list[i])
        else:
            object.reset_ftp_urls()
            for i in range(len(url_list)):
                if url_status_list[i] == 'allowed':
                    object.add_ftp_url_allowed(url_list[i])
                else:
                    object.add_ftp_url_denied(url_list[i])
    iterator.update_object(object)


def print_details_form(
    category,
    action,
    id,
    group='',
    ):
    """create table with user details"""

    if category == CATEGORY_USERS:
        id_name = _('User-ID')
    elif category == CATEGORY_HOSTS:
        id_name = _('IP-Address')
    elif category == CATEGORY_GROUPS:
        id_name = _('Group-ID')
    else:
        raise 'no valid category (%s)' % category
    new_action = ''
    if action == ACTION_EDIT_HTTP_PERMISSIONS:
        new_action = ACTION_SAVE_HTTP_PERMISSIONS
    elif action == ACTION_EDIT_FTP_PERMISSIONS:
        new_action = ACTION_SAVE_FTP_PERMISSIONS

    row_format = gui_misc.RowFormat()
    iterator = objectiterator.ObjectIterator(category)
    object = iterator.get_object(id)

    if category == CATEGORY_USERS or category == CATEGORY_HOSTS:
        colspan = 3
    else:
        colspan = 1

    html_string = '<form action="%s" method="post">\n' \
        % os.environ['SCRIPT_NAME']
    html_string += '<input type="hidden" name="action" value="%s">\n' \
        % new_action
    html_string += '<input type="hidden" name="category" value="%s">\n' \
        % category
    html_string += '<tr>'  # table started in head for resize
    html_string += '<th align=right><nobr>%s</nobr></th>\n' % id_name
    html_string += '<td class = "%s" colspan=%s>%s</td></tr>\n' \
        % (row_format.get_next_row_class(), colspan, id)
    html_string += '<input type="hidden" name="id" value="%s">\n' % id
    if category == CATEGORY_USERS or category == CATEGORY_HOSTS:
        html_string += '<tr><th align=right>%s</th>\n' % _('Group')
        html_string += '<td class = "%s" align=left colspan=%i>\n' \
            % (row_format.get_next_row_class(), colspan)
        html_string += \
            '<input type="hidden" name="group" value="%s">%s\n' \
            % (group, group)
        html_string += '</td></tr>\n'
        html_string += '<tr class = "%s">' \
            % row_format.get_next_row_class()
        html_string += '<th/><td align=left colspan=%i>%s</td>\n' \
            % (colspan,
               _('these rules have priority over the rules of the group'
               ))
        if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
            == ACTION_EDIT_FTP_PERMISSIONS:
            html_string += '<tr class = "%s"><th></th>\n' \
                % row_format.get_next_row_class()
            html_string += '<td align=left size="40">&nbsp;</td>\n'
            html_string += '<td align=center><b>%s</b></td>\n' \
                % _('allowed')
            html_string += '''<td align=center><b>%s</b></td>
</tr>
''' \
                % _('denied')
    else:
        status_allowed = ''
        status_denied = ''
        status_text = ''
        if action == ACTION_EDIT_HTTP_PERMISSIONS:
            if object.get_http_permissions().is_default_allow():
                status_allowed = ' checked'
            else:
                status_denied = ' checked'
        if action == ACTION_SAVE_HTTP_PERMISSIONS:
            if object.get_http_permissions().is_default_allow():
                status_text = _('allowed')
            else:
                status_text = _('denied')
        elif action == ACTION_EDIT_FTP_PERMISSIONS:
            if object.get_ftp_permissions().is_default_allow():
                status_allowed = ' checked'
            else:
                status_denied = ' checked'
        elif action == ACTION_SAVE_FTP_PERMISSIONS:
            if object.get_ftp_permissions().is_default_allow():
                status_text = _('allowed')
            else:
                status_text = _('denied')
        html_string += '<tr class = "%s"><th align=right>%s</th>\n' \
            % (row_format.get_next_row_class(), _('Default'))
        html_string += '<td align=left>\n'
        if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
            == ACTION_EDIT_FTP_PERMISSIONS:
            html_string += \
                '<input type="radio" name="default" value="%s" %s>%s\n' \
                % (ALLOWED, status_allowed, _('allowed'))
            html_string += \
                '''<input type="radio" name="default" value="%s" %s>%s</td>
</tr>
''' \
                % (DENIED, status_denied, _('denied'))
        else:
            html_string += '%s</td></tr>\n' % status_text
        html_string += '<tr class = "%s">\n' \
            % row_format.get_next_row_class()
        html_string += \
            '''<th/><td align=left><nobr>%s</nobr></td>
</tr>
''' \
            % _('the URLs below are exceptions to the Default')
    index = 1
    if category == CATEGORY_GROUPS:
        if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
            == ACTION_SAVE_HTTP_PERMISSIONS:
            url_list = object.get_http_permissions().get_url_list()
        else:
            url_list = object.get_ftp_permissions().get_url_list()
    else:
        if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
            == ACTION_SAVE_HTTP_PERMISSIONS:
            url_list = object.get_http_url_list()
        else:
            url_list = object.get_ftp_url_list()
    for url in url_list:
        html_string += \
            '<tr class = "%s"><th align=right><nobr>URL(%i):</nobr></th>\n' \
            % (row_format.get_next_row_class(), index)
        if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
            == ACTION_EDIT_FTP_PERMISSIONS:
            html_string += \
                '<td align=left><input type="text" name="url_list_%i" value="%s" class="url"></td>\n' \
                % (index, url)
        else:
            html_string += '<td align=left>%s</td>\n' % url
        if category != CATEGORY_GROUPS:
            status_allowed = ''
            status_denied = ''
            status_text = ''
            if action == ACTION_EDIT_HTTP_PERMISSIONS:
                if object.is_http_url_allowed(url):
                    status_allowed = ' checked'
                else:
                    status_denied = ' checked'
            if action == ACTION_SAVE_HTTP_PERMISSIONS:
                if object.is_http_url_allowed(url):
                    status_text = _('allowed')
                else:
                    status_text = _('denied')
            elif action == ACTION_EDIT_FTP_PERMISSIONS:
                if object.is_ftp_url_allowed(url):
                    status_allowed = ' checked'
                else:
                    status_denied = ' checked'
            elif action == ACTION_SAVE_FTP_PERMISSIONS:
                if object.is_ftp_url_allowed(url):
                    status_text = _('allowed')
                else:
                    status_text = _('denied')

            if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
                == ACTION_EDIT_FTP_PERMISSIONS:
                html_string += \
                    '<td align=center><input type="radio" name="url_status_list_%i" value="allowed"%s>\n' \
                    % (index, status_allowed)
                html_string += \
                    '<td align=center><input type="radio" name="url_status_list_%i" value="denied"%s>\n' \
                    % (index, status_denied)
            else:
                html_string += '<td align=center>%s' % status_text
        html_string += '''</td>
</tr>
'''
        index = index + 1
    if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
        == ACTION_EDIT_FTP_PERMISSIONS:
        if index + ADDITIONAL_URL_ROWS > MINIMUM_URL_ROWS:
            row_number = ADDITIONAL_URL_ROWS
        else:
            row_number = MINIMUM_URL_ROWS - index + 1
        for i in range(row_number):
            html_string += \
                '''<tr class = "%s">
<th align=right><nobr>%s(%i):</nobr></th>
''' \
                % (row_format.get_next_row_class(), _('URL'), index)
            html_string += \
                '<td align=left><input type="text" name="url_list_%i" value="" class="url"></td>\n' \
                % index
            if category == CATEGORY_USERS or category == CATEGORY_HOSTS:
                html_string += \
                    '<td align=center><input type="radio" name="url_status_list_%i" value="allowed"></td>\n' \
                    % index
                html_string += \
                    '<td align=center><input type="radio" name="url_status_list_%i" value="denied" checked></td>\n' \
                    % index
            html_string += '</tr>\n'
            index = index + 1
    if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
        == ACTION_SAVE_HTTP_PERMISSIONS:
        status_ssl_from_group = ''
        status_ssl_enabled = ''
        status_ssl_disabled = ''
        text_ssl = ''

# ....status_msn_from_group = ''
#        status_msn_enabled = ''
#        status_msn_disabled = ''

        text_msn = ''

        if category != CATEGORY_GROUPS:
            if object.is_ssl_from_group():
                status_ssl_from_group = ' checked'
                text_ssl = _('as group')
            elif object.is_ssl_enabled():
                status_ssl_enabled = ' checked'
                text_ssl = _('enabled')
            else:
                status_ssl_disabled = ' checked'
                text_ssl = _('disabled')
        else:
            if object.get_http_permissions().is_ssl_enabled():
                status_ssl_enabled = ' checked'
                text_ssl = _('enabled')
            else:
                status_ssl_disabled = ' checked'
                text_ssl = _('disabled')
            if object.get_http_permissions().is_msn_enabled():
                status_msn_enabled = ' checked'
                text_msn = _('enabled')
            else:
                status_msn_disabled = ' checked'
                text_msn = _('disabled')
        html_string += '<tr><th align=right>SSL:</th>\n'
        html_string += '<td class = "%s" align=left colspan=%s>\n' \
            % (row_format.get_next_row_class(), colspan)
        if category != CATEGORY_GROUPS:
            if action == ACTION_EDIT_HTTP_PERMISSIONS:
                html_string += \
                    '<input type="radio" name="ssl" value="%s"%s>%s&nbsp;\n' \
                    % (SSL_FROM_GROUP, status_ssl_from_group,
                       _('as group'))
        if action == ACTION_EDIT_HTTP_PERMISSIONS:
            html_string += \
                '<input type="radio" name="ssl" value="%s"%s>%s&nbsp;\n' \
                % (SSL_ENABLED, status_ssl_enabled, _('enabled'))
            html_string += \
                '<input type="radio" name="ssl" value="%s"%s>%s\n' \
                % (SSL_DISABLED, status_ssl_disabled, _('disabled'))
        else:

        #    html_string += '<tr><th align=right>MSN:</th>\n'
        #    html_string += '<td class = "%s" align=left colspan=%s>\n' % (row_format.get_next_row_class(),colspan)
        #    html_string += '<input type="radio" name="msn" value="%s"%s>%s&nbsp;\n' % (MSN_ENABLED, status_msn_enabled, _('enabled'))
        #    html_string += '<input type="radio" name="msn" value="%s"%s>%s\n' % (MSN_DISABLED, status_msn_disabled, _('disabled'))

            html_string += text_ssl

        #    html_string += '<tr><th align=right>MSN:</th>\n'
    #    html_string += '<td class = "even" align=left colspan=1>'
    #    html_string += text_msn

        html_string += '</tr></td></tr>\n'
    html_string += '<tr><td colspan="4" align="center">\n'
    if action == ACTION_EDIT_HTTP_PERMISSIONS or action \
        == ACTION_EDIT_FTP_PERMISSIONS:
        html_string += '<input type="submit" name="send" value="%s">\n' \
            % _('save')
        html_string += \
            '<input type="button" value="%s" onClick="window.close()">\n' \
            % _('cancel')
    else:
        html_string += \
            '<input type="button" value="%s" onClick="opener.location.reload();opener.focus();self.close();">\n' \
            % _('close window')
    html_string += '''</td></tr>
</table>
'''
    html_string += '</form></center>\n'
    html_string += '</body>\n'
    html_string += '<script>resizeWinTo( \'resize_div\' );</script>\n'
    html_string += '</html>'
    print (html_string)

