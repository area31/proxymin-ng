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

def print_details_page(category, action, id = '', description = '', group = '', active = '', error_message = ''):
    """show details of an object"""
    #in case there was invalid user input we must reset the action here
    if(action == ACTION_SAVE_CREATE):
        action = ACTION_CREATE
    elif(action == ACTION_SAVE_DELETE):
        action = ACTION_DELETE
    elif(action == ACTION_SAVE_EDIT):
        action = ACTION_EDIT
    
    if(category == CATEGORY_USERS):
        if(action == ACTION_CREATE):
            title = _('create new user')
        elif(action == ACTION_DELETE):
            title = _('delete user')
        elif(action == ACTION_EDIT):
            title = _('modify user details')
        else:
            raise 'no valid action (%s)' %(action)
    elif(category == CATEGORY_HOSTS):
        if(action == ACTION_CREATE):
            title = _('create new host')
        elif(action == ACTION_DELETE):
            title = _('delete host')
        elif(action == ACTION_EDIT):
            title = _('modify host details')
        else:
            raise 'no valid action (%s)' %(action)
    elif(category == CATEGORY_GROUPS):
        if(action == ACTION_CREATE):
            title = _('create new group')
        elif(action == ACTION_DELETE):
            title = _('delete group')
        elif(action == ACTION_EDIT):
            title = _('modify group details')
        else:
            raise 'no valid action (%s)' %(action)
    else:
        raise 'no valid category (%s)' %(category)

    gui_misc.print_popup_head(2, title, error_message)

    if((error_message == '') and (action != ACTION_CREATE)):
        # object already exists
        iterator = objectiterator.ObjectIterator(category)
        object = iterator.get_object(id)
        if(category == CATEGORY_USERS or category == CATEGORY_HOSTS):
            group = object.get_group()
            active = object.is_enabled()         
        description = object.get_description()

    print_details_form(category,action, id, description, group, active)

def print_confirmation_page(error_message, category, action, id, description, group, active):
    """show user details"""
    if(error_message != ''):
        title = _('Error')
    elif(category == CATEGORY_USERS):
        if(action == ACTION_SAVE_CREATE):
            title = _('user created')
        elif(action == ACTION_SAVE_DELETE):
            title = _('user deleted')
        elif(action == ACTION_SAVE_EDIT):
            title = _('user modified')
        else:
            raise 'no valid action (%s)' %(action)
    elif(category == CATEGORY_HOSTS):
        if(action == ACTION_SAVE_CREATE):
            title = _('host created')
        elif(action == ACTION_SAVE_DELETE):
            title = _('host deleted')
        elif(action == ACTION_SAVE_EDIT):
            title = _('host modified')
        else:
            raise 'no valid action (%s)' %(action)
    elif(category == CATEGORY_GROUPS):
        if(action == ACTION_SAVE_CREATE):
            title = _('group created')
        elif(action == ACTION_SAVE_DELETE):
            title = _('group deleted')
        elif(action == ACTION_SAVE_EDIT):
            title = _('group modified')
        else:
            raise 'no valid action (%s)' %(action)
    else:
        raise 'no valid category (%s)' %(category)
        
    gui_misc.print_popup_head(2, title, error_message)
    print_details_form(category,action, id, description, group, active)

def validate_input_data(category, action, id):
    """check if input data is valid"""
    if(category == CATEGORY_USERS):
        id_name = _('User-ID')
    elif(category == CATEGORY_HOSTS):
        id_name = _('IP-Address')
    else:
        id_name = _('Group-ID')
    error_message = ''

    iterator = objectiterator.ObjectIterator(category)
    # is id available?
    if(id == ''):
        error_message = id_name + ' ' + _('is missing')
    # id only must contain alphanumeric characters and '_'
    elif(category != CATEGORY_HOSTS and not gui_misc.is_alphanum(id)):
        error_message = id_name + ' ' + _('only alphanumeric charactes and "_" are allowed')
    # check if valid IP
    elif(category == CATEGORY_HOSTS and not gui_misc.is_ip(id)):
        error_message = _('no valid IP-Address')
#    elif(category == CATEGORY_USERS and passwd1 != passwd2):
#        error_message = _('passwords do not match')
#    elif(category == CATEGORY_USERS and passwd1 == ''):
#        error_message = _('no password specified')
#    elif(category == CATEGORY_USERS and
#         action == ACTION_SAVE_EDIT and not
#         (gui_misc.is_alphanum(passwd1) or passwd1 == PASSWORD_UNCHANGED)):
#        error_message = _('ass password only alpanumeric characters and "_" are allowed')
    # is id already in use?
    elif(action == ACTION_SAVE_CREATE):
        if id in iterator.get_object_id_list():
            error_message = id_name + ' ' + _('already exists')
    return error_message

def save_input_data(category, id, description, group = '', active = FALSE):
    iterator = objectiterator.ObjectIterator(category)
    # check if object already exists, if not, then create it
    if not(iterator.get_object(id)):
        iterator.add_object(id)
    object = iterator.get_object(id)
#    if(category == CATEGORY_USERS):
    object.set_description(description)
    if(category != CATEGORY_GROUPS):
        object.set_group(group)
        if(active):
            object.enable()
        else:
            object.disable()
    iterator.update_object(object)

def delete_object(category, id):
    iterator = objectiterator.ObjectIterator(category)
    return iterator.delete_object(id)

def print_details_form(category,action, id='', description='', group='', active=TRUE):
    """create table with user details"""
    if(category == CATEGORY_USERS):
        id_name = _('User-ID')
    elif(category == CATEGORY_HOSTS):
        id_name = _('IP-Address')
    elif(category == CATEGORY_GROUPS):
        id_name = _('Group-ID')
    else:
        raise 'no valid category (%s)' % (category)        
    if(action == ACTION_CREATE):
        new_action = ACTION_SAVE_CREATE
    elif(action == ACTION_EDIT):
        new_action = ACTION_SAVE_EDIT
    elif(action == ACTION_DELETE):
        new_action = ACTION_SAVE_DELETE
    elif(action == ACTION_SAVE_CREATE or
         action == ACTION_SAVE_EDIT or
         action == ACTION_SAVE_DELETE):
        new_action = action # in case we revisit this place because of invalid user input
    else:
        raise 'no valid action (%s)' % (action)

    row_format = gui_misc.RowFormat()

    html_string = '<form action="%s" method="post">\n' % (os.environ['SCRIPT_NAME'])
    html_string += '<input type="hidden" name="action" value="%s">\n' % (new_action)
    html_string += '<input type="hidden" name="category" value="%s">\n' % (category)
    html_string += '<tr><th align=right><nobr>%s</nobr></th>\n' % (id_name)
    if(action == ACTION_CREATE):
        html_string += '<td class = "%s" align=left><input type="text" name="id"' % (row_format.get_next_row_class())
        html_string += ' value="%s"></td></tr>\n' % (id)
    else: # uid can only be changed while creation
        html_string += '<td class = "%s" align=left><input type="hidden" name="id"' % (row_format.get_next_row_class())
        html_string += ' value="%s"><nobr>%s</nobr></td></tr>\n' % (id, id)
    html_string += '<tr><th align=right>%s</th>\n' % (_('Description'))
    if(action == ACTION_CREATE or action == ACTION_EDIT):
        html_string += '<td class = "%s" align=left><input type="text"' % row_format.get_next_row_class()
        html_string += 'name="description" value="%s" class="description"></td></tr>\n' % (description)
    else:
        html_string += '<td class = "%s" align=left><nobr>%s</nobr></td></tr>\n' % (row_format.get_next_row_class(), description)
    if(category == CATEGORY_USERS or category == CATEGORY_HOSTS):   
        html_string += '<tr><th align=right>%s</th>\n' %(_('Group'))
        html_string += '<td class = "%s" align=left>' % (row_format.get_next_row_class())
        if(action == ACTION_CREATE or action == ACTION_EDIT):
            html_string += gui_misc.group_selector(group)
        else:
            html_string += '<input type="hidden" name="group" value="%s">%s' % (group, group)
        html_string += '</td>\n</tr>\n'    
    if(category == CATEGORY_USERS or category == CATEGORY_HOSTS):   
        html_string += '<tr><th align=right>%s</th>' % (_('active'))
        html_string += '<td class = "%s" align=left>'% (row_format.get_next_row_class())
        if(action == ACTION_CREATE or action == ACTION_EDIT):
            html_string += '<input type="checkbox" name="active"' 
            if(active):
                html_string += 'checked="checked"'
        else:
            if(active):
                html_string += _('yes')
                html_string += '<input type="hidden" name="active" value="on">'
            else:
                html_string += _('no')
        html_string += '</td>\n</tr>\n'
    html_string += '<tr><td colspan="2" align="center">'
    if(action == ACTION_CREATE or action == ACTION_EDIT or action == ACTION_DELETE):
        if(action == ACTION_CREATE or action == ACTION_EDIT):
            button_label = _('save')
        else:
            button_label = _('delete')
        html_string += '<input type="submit" name="send" value="%s">\n' % (button_label)
        html_string += '<input type="button" value="%s" onClick="window.close()"></td>\n</tr>\n' % (_('cancel'))
    else:
        html_string += '<input type="button" value="%s"' % (_('close window'))
        html_string += 'onClick="opener.location.reload();opener.focus();self.close();">\n'
    html_string += '</table>\n'
    html_string += '</center></form>\n'
    html_string += '</body>\n'
    html_string += '<script>resizeWinTo(\'resize_div\');</script>\n'
    html_string += '</html>'
    print (html_string)
