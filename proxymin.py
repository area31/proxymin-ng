#!/usr/bin/python
# -*- coding: latin-1 -*-

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

import cgitb; cgitb.enable()

import cgi
import dbaccess
import string
import sys

import gui_bandwidth
import gui_msn
import gui_extensions
import gui_help
import gui_info
import gui_main
import gui_misc
import gui_permission_details
import ConfigParser
from localization import _
from globals import *

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE_PATH + CONFIG_FILE)
global user_password
user_password = config.get("password","user_password")

if user_password == 'yes':
    import gui_object_details_USRPWD as gui_object_details
else:
    import gui_object_details_NOUSRPWD as gui_object_details

"""process request, extract POST/GET vars and call appropriate functions"""
#set defaults
action = ACTION_SHOW_MAIN
category = CATEGORY_GROUPS
id = ''
group = None
description = ''
passwd1 = ''
passwd2 = ''
active = FALSE
letter = None
url_list = []
url_status_list = []
ssl = ''
msn = ''
bandwidth_limit = ''
default = ''
extension_list = []
# extract all POST and FORM values    
form = cgi.FieldStorage()
# extract parameters
if form.has_key('action'):
    action = form['action'].value
if form.has_key('category'):
    category = form['category'].value
if form.has_key('id'):
    id = form['id'].value
if form.has_key('group'):
    group = form['group'].value
if form.has_key('description'):
    description = form['description'].value
if form.has_key('passwd1'):
    passwd1 = form['passwd1'].value
if form.has_key('passwd2'):
    passwd2 = form['passwd2'].value
if form.has_key('active'):
    active = form['active'].value
if form.has_key('letter'):
    letter = form['letter'].value
if form.has_key('ssl'):
    ssl = form['ssl'].value
if form.has_key('msn'):
    msn = form['msn'].value
if form.has_key('bandwidth_limit'):
    bandwidth_limit = form['bandwidth_limit'].value
if form.has_key('default'):
    default = form['default'].value
for key in form.keys():
    if key[:9] == 'url_list_':
        index = int(key[9:])
        url_list.append(form['url_list_%i' % index].value)
        # group has no url status
        if form.has_key('url_status_list_%i' % index):
            url_status_list.append(form['url_status_list_%i' % index].value)
    elif key[:15] == 'extension_list_':
        index = int(key[15:]) 
        extension_list.append(form['extension_list_%i' % index].value)
            
print 'Content-type: text/html\n\n'
# call appropriate page
if(action == ACTION_SHOW_MAIN):
    gui_main.print_main_page(category, letter, group)
elif(action == ACTION_DISPLAY_HELP):
    gui_help.print_help_page()
elif(action == ACTION_DISPLAY_INFO):
    gui_info.print_info_page()       
else:
    if(action == ACTION_CREATE or
       action == ACTION_DELETE or
       action == ACTION_EDIT):
        dba = dbaccess.DBAccess()
#        if(category == CATEGORY_GROUPS and action == ACTION_DELETE and id == "Padrao"):
#            gui_object_details.print_confirmation_page(_('Voce nao pode apagar o grupo Padrao!Ã'),category, ACTION_SAVE_DELETE, id, description, group, active)
        if(category == CATEGORY_GROUPS and action == ACTION_DELETE and len(dba.get_group_list()) == 1):
            gui_object_details.print_confirmation_page(_('at least one group must exist'),category, ACTION_SAVE_DELETE, id, description, group, active)
        elif(category != CATEGORY_GROUPS and action == ACTION_CREATE and len(dba.get_group_list()) == 0):
            gui_object_details.print_confirmation_page(_('at first a group must be created'),CATEGORY_GROUPS, ACTION_CREATE, '', '', '', '')
        else:
            gui_object_details.print_details_page(category, action, id, '', '', TRUE)
    elif(action == ACTION_SAVE_CREATE or action == ACTION_SAVE_EDIT):
        if (user_password == 'yes'):
            error_message = gui_object_details.validate_input_data(category, action, id, passwd1, passwd2)
        else:
            error_message = gui_object_details.validate_input_data(category, action, id)
        if(error_message != ''):
            gui_object_details.print_details_page(category, action, id, description, group, active, error_message)
        else:
            if (user_password == 'yes'):
                gui_object_details.save_input_data(category, id, description, group, active, passwd1)
            else:
                gui_object_details.save_input_data(category, id, description, group, active)
            gui_object_details.print_confirmation_page('',category, action, id, description, group, active)
    elif(action == ACTION_SAVE_DELETE):
        if(gui_object_details.delete_object(category, id)):
            gui_object_details.print_confirmation_page('',category, action, id, description, group, active)
        elif(category == CATEGORY_GROUPS):
                gui_object_details.print_confirmation_page(_('the group could not be deleted'),category, action, id, description, group, active)
        else:
            gui_object_details.print_confirmation_page(_('the object could not be deleted'),category, action, id, description, group, active)                
    elif(action == ACTION_EDIT_HTTP_PERMISSIONS or action == ACTION_EDIT_FTP_PERMISSIONS):
        gui_permission_details.print_details_page(category, action, id)
    elif(action == ACTION_SAVE_HTTP_PERMISSIONS or action == ACTION_SAVE_FTP_PERMISSIONS):
        gui_permission_details.save_input_data(category, id, action, url_list, url_status_list, ssl, default)
        gui_permission_details.print_confirmation_page(category, id, action, group)
    elif(action == ACTION_EDIT_EXTENSIONS):
        gui_extensions.print_details_page(id)
    elif(action == ACTION_EDIT_MSN):
        gui_msn.print_details_page(id, category)
    elif(action == ACTION_EDIT_BANDWIDTH):
        gui_bandwidth.print_details_page(id, category)
    elif(action == ACTION_SAVE_EXTENSIONS):
        gui_extensions.save_input_data(id, extension_list)
        gui_extensions.print_confirmation_page(id, extension_list)
    elif(action == ACTION_SAVE_MSN):
        gui_msn.save_input_data(id, category, msn)
        gui_msn.print_confirmation_page(id, category, msn)
    elif(action == ACTION_SAVE_BANDWIDTH):
        gui_bandwidth.save_input_data(id, category, bandwidth_limit)
        gui_bandwidth.print_confirmation_page(id, category, bandwidth_limit)
