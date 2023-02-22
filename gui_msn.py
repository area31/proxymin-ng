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

import ConfigParser

import permissions
import dbaccess
import gui_misc
import objectiterator
from globals import *
from localization import _

def print_details_page(id, category):
    """show http/ftp details of an object"""
    title = _('Instant Messaging Permissions')
    gui_misc.print_popup_head(2, title)
    print_details_form(id, category, ACTION_EDIT_MSN)

def print_confirmation_page(id, category, msn):
    """confirm successful changes"""
    title = _('your changes have been saved')
    gui_misc.print_popup_head(2, title)
    print_details_form(id, category, ACTION_SAVE_MSN)

def save_input_data(id, category, msn):
#    row_format = gui_misc.RowFormat()
    iterator = objectiterator.ObjectIterator(category)
    object = iterator.get_object(id)

    if category == CATEGORY_GROUPS:
    	if(msn == MSN_ENABLED):
    		object.get_http_permissions().enable_msn()
    	else:
      		object.get_http_permissions().disable_msn()
    else:
	if(msn == MSN_ENABLED):
    		object.enable_msn()
    	elif(msn == MSN_DISABLED):
      		object.disable_msn()
	else: 
		#Msn group default
		object.reset_msn()

    iterator.update_object(object)

def print_details_form(id, category, action):
    """create table with user details"""
    row_format = gui_misc.RowFormat()
    iterator = objectiterator.ObjectIterator(category)
    object = iterator.get_object(id)
    status_msn_from_group = ''
    status_msn_disabled = ''
    status_msn_enabled = ''
    #Object for Category is groups or users/hosts
    if category == CATEGORY_GROUPS:
    	if(object.get_http_permissions().is_msn_enabled()):
          	status_msn_enabled = ' checked'
          	text_msn = _('enabled')
    	else:
          	status_msn_disabled = ' checked'
          	text_msn = _('disabled')
    else:
	if(object.is_msn_from_group()):
        	status_msn_from_group = ' checked'
        	text_msn = _('as group')
   	elif(object.is_msn_enabled()):
        	status_msn_enabled = ' checked'
        	text_msn = _('allowed')
	else:
        	status_msn_disabled = ' checked'
        	text_msn = _('denied')
    
    colspan = 1
    html_string = ''
    html_string += '<form action="%s" method="post">\n' % (os.environ['SCRIPT_NAME'])
    html_string += '<input type="hidden" name="action" value="%s">\n' % (ACTION_SAVE_MSN)
    html_string += '<input type="hidden" name="category" value="%s">\n' % (category)
    html_string += '<tr>' # table started in head for resize
    html_string += '<tr class = "%s"><th align=right>%s:</th>\n' % (row_format.get_next_row_class(), _('Group-ID'))
    html_string += '<td align=left><input type="hidden" name="id"'
    html_string += ' value="%s">%s</td></tr>\n' % (id, id)
    html_string += '<tr><th align=right>MSN / ICQ / GTALK:</th>\n'
#    html_string += '<td class = even align=left colspan=1>'
    html_string += '<td class = "%s" align=left colspan=%s>\n' % (row_format.get_next_row_class(),colspan)
    if (category != CATEGORY_GROUPS):
    	html_string += '<input type="radio" name="msn" value="%s"%s>%s&nbsp;' % (MSN_FROM_GROUP, status_msn_from_group, _('as group'))
    html_string += '<input type="radio" name="msn" value="%s"%s>%s&nbsp;' % (MSN_ENABLED, status_msn_enabled, _('allowed'))
    html_string += '<input type="radio" name="msn" value="%s"%s>%s\n' % (MSN_DISABLED, status_msn_disabled, _('denied'))
    html_string += '</tr></td></tr>\n'
    html_string += '<tr><td colspan="4" align="center">\n'
    if(action == ACTION_EDIT_MSN):
        html_string += '<input type="submit" name="send" value="%s">\n' % (_('save'))
        html_string += '<input type="button" value="%s" onClick="window.close()">\n' % (_('cancel'))
    else:
        html_string += '<input type="button" value="%s" onClick="opener.location.reload();opener.focus();self.close();">' % (_('close window'))
    html_string += '</td>\n</tr>\n</table>\n'
    html_string += '</center></form>\n'
    html_string += '</body>\n'
    html_string += '<script>resizeWinTo( \'resize_div\' );</script>\n'
    html_string += '</html>'
    print html_string
