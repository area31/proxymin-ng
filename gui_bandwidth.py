# -*- coding: latin-1 -*-

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

import permissions
import dbaccess
import gui_misc
import objectiterator
from globals import *
from localization import _


def print_details_page(id, category):
    """show bandwidth details of an object"""

    title = _('Bandwidth Limit Permissions')
    gui_misc.print_popup_head(2, title)
    print_details_form(id, category, ACTION_EDIT_BANDWIDTH)


def print_confirmation_page(id, category, limit):
    """confirm successful changes"""

    title = _('your changes have been saved')
    gui_misc.print_popup_head(2, title)
    print_details_form(id, category, ACTION_SAVE_BANDWIDTH)


def save_input_data(id, category, limit):

#    row_format = gui_misc.RowFormat()

    iterator = objectiterator.ObjectIterator(category)
    object = iterator.get_object(id)

    object.set_bandwidth_limit(limit)

    iterator.update_object(object)


def print_details_form(id, category, action):
    row_format = gui_misc.RowFormat()
    iterator = objectiterator.ObjectIterator(category)
    object = iterator.get_object(id)

    colspan = 1
    html_string = ''
    html_string += '<form action="%s" method="post">\n' \
        % os.environ['SCRIPT_NAME']
    html_string += '<input type="hidden" name="action" value="%s">\n' \
        % ACTION_SAVE_BANDWIDTH
    html_string += '<input type="hidden" name="category" value="%s">\n' \
        % category
    html_string += '<tr>'  # table started in head for resize
    html_string += '<tr class = "%s"><th align=right>%s:</th>\n' \
        % (row_format.get_next_row_class(), _('Group-ID'))
    html_string += '<td align=left><input type="hidden" name="id"'
    html_string += ' value="%s">%s</td></tr>\n' % (id, id)
    html_string += '<tr><th align=right>%s:</th>\n' \
        % _('Bandwidth limit')
    html_string += '<td class = "%s" align=left colspan=%s>\n' \
        % (row_format.get_next_row_class(), colspan)

    if action == ACTION_EDIT_BANDWIDTH:
        html_string += \
            '<input type="text" name="bandwidth_limit" value="%s">' \
            % object.bandwidth_limit
    else:
        html_string += '%s' % object.bandwidth_limit

    if action == ACTION_SAVE_BANDWIDTH \
        and object.is_bandwidth_limit_disabled():
        html_string += ' %s\n' % _('default')
    else:
        html_string += ' %s\n' % _('in kbytes')

    html_string += '</tr></td></tr>\n'

    # Observaï¿½ï¿½o

    html_string += '<tr><th align=right>OBS.:</th>\n'
    html_string += '<td class = "%s" align=left colspan=%s>\n' \
        % (row_format.get_next_row_class(), colspan)
    if category == CATEGORY_GROUPS:
        html_string += \
            '- O limite \xef\xbf\xbd para cada usu\xef\xbf\xbdrio/host do grupo.<br/>'
    html_string += \
        '- O limite do usu\xef\xbf\xbdrio/host prevalece sobre o do grupo.'

    html_string += '<tr><td colspan="4" align="center">\n'
    if action == ACTION_EDIT_BANDWIDTH:
        html_string += '<input type="submit" name="send" value="%s">\n' \
            % _('save')
        html_string += \
            '<input type="button" value="%s" onClick="window.close()">\n' \
            % _('cancel')
    else:
        html_string += \
            '<input type="button" value="%s" onClick="opener.location.reload();opener.focus();self.close();">' \
            % _('close window')
    html_string += '''</td>
</tr>
</table>
'''
    html_string += '</center></form>\n'
    html_string += '</body>\n'
    html_string += '<script>resizeWinTo( \'resize_div\' );</script>\n'
    html_string += '</html>'
    print (html_string)

