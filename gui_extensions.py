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

def print_details_page(id):
    """show http/ftp details of an object"""
    title = _('forbid file extensions')
    gui_misc.print_popup_head(2, title)
    print_details_form(id, ACTION_EDIT_EXTENSIONS)

def print_confirmation_page(id, extension_list):
    """confirm successful changes"""
    title = _('your changes have been saved')
        
    gui_misc.print_popup_head(2, title)
    print_details_form(id, ACTION_SAVE_EXTENSIONS)

def save_input_data(id, extension_list):
    row_format = gui_misc.RowFormat()
    dba = dbaccess.DBAccess()
    group = dba.get_group(id)
    group.flush_denied_extensions()
    for extension in extension_list:
        group.deny_extension(extension)
    dba.update_group(group)

def print_details_form(id, action):
    """create table with user details"""
    row_format = gui_misc.RowFormat()
    dba = dbaccess.DBAccess()
    group = dba.get_group(id)

    html_string = ''
    html_string += '<form action="%s" method="post">\n' % (os.environ['SCRIPT_NAME'])
    html_string += '<input type="hidden" name="action" value="%s">\n' % (ACTION_SAVE_EXTENSIONS)
    html_string += '<tr class = "%s"><th align=right>%s:</th>\n' % (row_format.get_next_row_class(), _('Group-ID'))
    html_string += '<td align=left><input type="hidden" name="id"'
    html_string += ' value="%s">%s</td></tr>\n' % (id, id)
    index = 1        
    for extension in group.get_denied_extensions_list():
        html_string += '<tr class = "%s"><th align=right>%s(%i):</th>\n' % (row_format.get_next_row_class(), _('Extension'), index)
        if(action == ACTION_EDIT_EXTENSIONS):
            html_string += '<td align=left><input type="text" name="extension_list_%i" value="%s" class="extension">' % (index, extension)
        else:
            html_string += '<td align=left>%s' % (extension)
        html_string += '</td>\n</tr>\n'
        index = index + 1
    if(action == ACTION_EDIT_EXTENSIONS):        
        if(index + ADDITIONAL_URL_ROWS > MINIMUM_URL_ROWS):
            row_number = ADDITIONAL_URL_ROWS
        else:
            row_number = MINIMUM_URL_ROWS - index + 1

        for i in range(row_number):
            html_string += '<tr class = "%s"><th align=right>%s(%i):</th>\n' % (row_format.get_next_row_class(), _('Extension'), index)
            html_string += '<td align=left><input type="text" name="extension_list_%i" value="" class="extension"></td>\n' % (index)
            index = index + 1
    html_string += '<tr><td colspan="2" align="center">\n'
    if(action == ACTION_EDIT_EXTENSIONS):
        html_string += '<input type="submit" name="send" value="%s">\n' % (_('save'))
        html_string += '<input type="button" value="%s" onClick="window.close()">\n' % (_('cancel'))
    else:
        html_string += '<input type="button" value="%s" onClick="opener.location.reload();opener.focus();self.close();">' % (_('close window'))
    html_string += '</td>\n</tr>\n</table>\n'
    html_string += '</center></form>\n'
    html_string += '</body>\n'
    html_string += '<script>resizeWinTo( \'resize_div\' );</script>\n'
    html_string += '</html>'
    print (html_string)
