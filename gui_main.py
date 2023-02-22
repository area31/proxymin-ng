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
import os
import string
import time

import gui_misc
import objectiterator
from globals import *
from localization import _

def print_main_page(category, letter, group):
    """display administration main page"""    
    gui_misc.print_html_head()       
    print_title_bar()
    print '<br><br>'
    print_tabs(category)
    print '<br>'
    alphabet(category, group) 
    print '<br>'
    print_object_table(category, letter, group)
    print '<br>'
    gui_misc.print_footer()

def alphabet(category, group=None):
    print '<center>'   
    print '<a href="%s">%s</a>' % (os.environ['SCRIPT_NAME'] + format_post_vars(category, None, group), _('All')) 
    print '| <a href="%s">0-9</a>' % (os.environ['SCRIPT_NAME'] + (format_post_vars(category, string.digits, group)))   
    for i in range(0,26):
        print '| <a href="%s">%s</a>' \
         % (os.environ['SCRIPT_NAME'] + (format_post_vars(category, string.lowercase[i], group)), string.lowercase[i])
    print '</center>'

def print_title_bar():
    # count all user/host/group objects
    iterator = objectiterator.ObjectIterator(CATEGORY_HOSTS)
    number_of_hosts = iterator.get_object_count()
    iterator.set_category(CATEGORY_USERS)
    number_of_users = iterator.get_object_count()
    iterator.set_category(CATEGORY_GROUPS)
    number_of_groups = iterator.get_object_count()
    values = {'program_name':PROGRAM_NAME,
              'program_version':PROGRAM_VERSION,
              'script_name':os.environ['SCRIPT_NAME'],
              'query_string':os.environ['QUERY_STRING'],
              'window_help':WINDOW_HELP,
              'window_info':WINDOW_INFO,
              'action_display_help':ACTION_DISPLAY_HELP,
              'action_display_info':ACTION_DISPLAY_INFO,
              'number_of_hosts':number_of_hosts,
              'number_of_users':number_of_users,
              'number_of_groups':number_of_groups,
              'date_time':time.strftime('%d.%m.%y - %H:%M:%S'),
              'reload':_('Reload'),
              'help':_('Help'),
              'info':_('Info'),
              'hosts':_('Hosts'),
              'users':_('Users'),
              'groups':_('Groups'),
              'statistics':_('Statistics'),
              'page_help_height':PAGE_HELP_HEIGHT,
              'page_help_width':PAGE_HELP_WIDTH,
              'page_info_height':PAGE_INFO_HEIGHT,
              'page_info_width':PAGE_INFO_WIDTH}
    template = """
<body>
<table cellpadding=10 cellspacing=0 border=0 width="100%%">
  <tr class="titlebar">
    <td class="title">%(program_name)s - v%(program_version)s</td>
    <td class="links"><nobr>
      [ <a href="%(script_name)s?%(query_string)s">%(reload)s</a> ]
    </td>
  </tr>
  <tr class="statusbar">
    <td COLSPAN="2"><b>%(statistics)s:</b> %(number_of_hosts)i %(hosts)s; %(number_of_users)i %(users)s; %(number_of_groups)i %(groups)s (%(date_time)s)</td>
  </tr>
</table>"""
    print template % values

def print_tabs(category = CATEGORY_HOSTS):
    id_tab_users = 'inactive'   
    id_tab_hosts = 'inactive'       
    id_tab_groups = 'inactive'      
    if(category == CATEGORY_USERS):
        id_tab_users = 'active'   
    elif(category == CATEGORY_HOSTS):
        id_tab_hosts = 'active'       
    elif(category == CATEGORY_GROUPS):
        id_tab_groups = 'active'
    else:
        raise 'no valid category (%s)' %(category)        
    values = {'id_tab_users':id_tab_users,
              'id_tab_hosts':id_tab_hosts,
              'id_tab_groups':id_tab_groups,
              'category_users':CATEGORY_USERS,
              'category_hosts':CATEGORY_HOSTS,
              'category_groups':CATEGORY_GROUPS,
              'hosts':_('Hosts'),
              'users':_('Users'),
              'groups':_('Groups')}
    template = """
<table border="0" cellspacing="0" cellpadding="3" width="100%%" class="tabs" >
  <tr class="tabs">
    <td/>
    <td class="tab" id="%(id_tab_hosts)s" width="20%%">
      <a href="?category=%(category_hosts)s">%(hosts)s</a>
    </td>
    <td width="1%%"/>
    <td class="tab" id="%(id_tab_users)s" width="20%%">
      <a href="?category=%(category_users)s">%(users)s</td>
    <td width="1%%"/>
    <td class="tab" id="%(id_tab_groups)s" width="20%%">
      <a href="?category=%(category_groups)s">%(groups)s</td>
    <td/>
  </tr>
</table>"""
    print template % values

def display_protocol_info(object, category, protocol):
    """display http properties formated"""
    if(category != CATEGORY_GROUPS):
        if(protocol == PROTOCOL_HTTP):
            url_list = object.get_http_url_list()
        else: # protocol == PROTOCOL_FTP
            url_list = object.get_ftp_url_list()            
        if url_list:
            return '<font id="changed">%s</font>' % (_('adapted'))
        else:
            return '<font id="standard">%s</font>' % (_('default'))
    else: # category = CATEGORY_GROUPS
        if(protocol == PROTOCOL_HTTP):
            perm = object.get_http_permissions()
        else: # protocol == PROTOCOL_FTP
            perm = object.get_ftp_permissions()
        if perm.is_unrestricted():
            return '<font id="enabled">%s</font>' % (_('allowed'))
        elif perm.is_restricted():
            return '<font id="changed">%s</font>' % (_('limited'))
        elif perm.is_disabled():
            return '<font id="disabled">%s</font>' % (_('denied'))

def display_status_info(object):
    """display account status information formated"""        
    if object.is_enabled():
        return '<font id="enabled">%s</font>' % (_('enabled'))
    else:
        return '<font id="disabled">%s</font>' % (_('disabled'))

def display_group_name(object):
    """display objects group formated"""        
    if object.get_group():
        return '<font id="enabled">'+ object.get_group() +'</font>'
    else:
        return '<font id="changed">%s</font>' % (_('none'))       

def display_extension_info(object):
    """display if all extensions are allowed"""        
    if object.get_denied_extensions_list():
        return '<font id="changed">%s</font>' % (_('limited'))
    else:
        return '<font id="enabled">%s</font>' % (_('all allowed'))

def display_msn_info(object, category):
	"""display if msn are allowed"""        
	if category == CATEGORY_GROUPS:
		if(object.get_http_permissions().is_msn_enabled()):
			return '<font id="enabled">%s</font>' % (_('allowed'))
		else:
			return '<font id="disabled">%s</font>' % (_('denied'))
	else:
		if(object.is_msn_from_group()):
			return '<font id="standard">%s</font>' % (_('default'))
		elif(object.is_msn_enabled()):
			return '<font id="enabled">%s</font>' % (_('allowed'))
		else:
			return '<font id="disabled">%s</font>' % (_('denied'))

def display_bandwidth_limit_info(object):
    """display if bandwidth was seted"""
    if object.is_bandwidth_limit_disabled():
        return '<img src="%s?%s=%s" style="vertical-align: middle;"> <font id="standard">%s</font>' % (IMAGE_SCRIPT, IMAGE_GET_VARIABLE, IMAGE_BALL_RED, _('default'))
    else:
        return '%s %s' % (object.bandwidth_limit, _('in kbytes'))

def format_post_vars(category, letter, group):
    """create string to append at URL according to the supplied post variables"""
    post_vars = ""
    first_var = TRUE
    if category:    
        post_vars = "?category=" + category
        first_var = FALSE    
    if letter:       
        if first_var:
            post_vars = post_vars + "?"
        else:
            post_vars = post_vars + "&"
        post_vars = post_vars + "letter=" + letter
        first_var = FALSE        
    if group:
        if first_var:
            post_vars = post_vars + "?"
        else:
            post_vars = post_vars + "&"
        post_vars = post_vars + "group=" + group
    return post_vars

def print_group_selector(category, letter, default_group):
    """drop down select to restrict shown users/hosts to a certain group"""
    dba = dbaccess.DBAccess()
    html_string = '<form action=""><th>\n'
    html_string += '<table cellspacing="0" cellpadding="0" border=0"><tr><td><b>%s&nbsp;</b></td>\n' % (_('Group'))
    html_string += '<td><select name="group_selection"'
    html_string += ' onChange="go(this.form.group_selection.options[this.form.group_selection.options.selectedIndex].value)">\n'
    # create select box, "option value" is the complete target link
    html_string += '<option value="%s"' % (os.environ['SCRIPT_NAME'] + format_post_vars(category, letter, None))
    if(default_group == None):
        html_string += ' selected'
    html_string += '>%s</option>\n' % (_('All'))     
    for g in dba.get_group_list():
        html_string += '<option value="%s"' % (format_post_vars(category, letter, g))
        if default_group == g:
            html_string += ' selected'
        html_string += '>%s</option>\n' % (g)
    html_string += '</select>\n'    
    html_string += '</td></tr></table>\n'
    html_string += '</th></form>'
    print html_string

def print_object_table(category, letter, group):
    """create center table of main administration screen"""
    aca=dbaccess.DBAccess()
    iterator = objectiterator.ObjectIterator(category)

    row_format = gui_misc.RowFormat()
    
    if(category == CATEGORY_USERS):
        id_type = _('User-ID')
        create_new = _('create new user')
        colspan_footer = 9
    elif(category == CATEGORY_HOSTS):
        id_type = _('IP-Address')
        create_new = _('create new host')
        colspan_footer = 9
    elif(category == CATEGORY_GROUPS):
        id_type = _('Group-ID')
        create_new = _('create new group')
        colspan_footer = 8
    else:
        raise 'no valid category (%s)' %(category)        

    html_string = '<center>\n'
    html_string += '<table  cellspacing="2" cellpadding="3">\n'
    html_string += '<tr>\n'
    html_string += '<th>Nr.</th>\n'
    html_string += '<th>%s</th>\n' % (id_type)
    html_string += '<th>%s</th>\n' % _('Description')
    html_string += '<th>%s</th>\n' % _('Bandwidth limit')
    print html_string 
    if category != CATEGORY_GROUPS:
        print_group_selector(category, letter, group)
    html_string = '<th>HTTP</th>'
    html_string += '<th>FTP</th>'
    if category == CATEGORY_GROUPS:
        html_string += '<th>%s</th>\n' % (_('Extensions'))
	# Add msn header for groups
	html_string += '<th>%s</th>\n' % (_('MSN'))
	# end msn header
    else:    
       	# Add msn header for users/hosts
	html_string += '<th>%s</th>\n' % (_('MSN'))
	# end msn header
	html_string += '<th>%s</th>\n' % (_('Status'))

    html_string += '<th>%s</TH>\n' % (_('Modify'))
    html_string += '<th/>\n'
    html_string += '</tr>\n'
    print html_string
    
    html_string = ''  
    objlist = iterator.get_object_id_list(letter, group)
    i = 1 # object counter
    for id in objlist:          
        object = iterator.get_object(id)         
        html_string += '<tr class = "%s">\n' % (row_format.get_next_row_class())
        html_string += '<td>%s</td>\n' % repr(i)
        html_string += '<td>%s</td>\n' % id 
        html_string += '<td>%s</td>\n' % object.get_description()
        html_string += '<td>%s</td>\n' % display_bandwidth_limit_info(object)
        if category != CATEGORY_GROUPS:
            html_string += '<td>%s</td>\n' % display_group_name(object)
        html_string += '<td><table cellspacing="0" cellpadding="0" border=0"><tr><td>'
        if iterator.is_default_allow(object, PROTOCOL_HTTP):
            html_string += '<img src="%s?%s=%s">' % (IMAGE_SCRIPT, IMAGE_GET_VARIABLE, IMAGE_BALL_GREEN)
        else:
            html_string += '<img src="%s?%s=%s">' % (IMAGE_SCRIPT, IMAGE_GET_VARIABLE, IMAGE_BALL_RED)
        html_string += '</td><td>&nbsp;%s</td></tr></table></td>\n' % display_protocol_info(object, category, PROTOCOL_HTTP) 
        html_string += '<td><table cellspacing="0" cellpadding="0" border=0"><tr><td>' 
        if iterator.is_default_allow(object, PROTOCOL_FTP):
            html_string += '<img src="%s?%s=%s">' % (IMAGE_SCRIPT, IMAGE_GET_VARIABLE, IMAGE_BALL_GREEN)
        else:
            html_string += '<img src="%s?%s=%s">' % (IMAGE_SCRIPT, IMAGE_GET_VARIABLE, IMAGE_BALL_RED)
        html_string += '<td>&nbsp;%s</td></tr></table></td>\n' % display_protocol_info(object, category, PROTOCOL_FTP)    
        if category != CATEGORY_GROUPS:
  	    # First MSN menu (for users/hosts only)
	    html_string += '<td>%s</td>\n' % display_msn_info(object, category)
	    # End first msn menu
            html_string += '<td>%s</td>\n' % display_status_info(object)
        else:
            html_string += '<td>%s</td>\n' % display_extension_info(object)
	    # First MSN menu (for groups only)
	    html_string += '<td>%s</td>\n' % display_msn_info(object, category)
	    # End first msn menu

        html_string += '<td>\n'
        html_string += '<A href="%s?action=%s&id=%s&category=%s" target="%s"' \
                       % (os.environ['SCRIPT_NAME'],ACTION_EDIT,id,category,WINDOW_DETAILS)
        html_string += 'onClick=popup("%s")>%s</a>&nbsp;\n' % (WINDOW_DETAILS, _('Details'))       
        html_string += '<A href="%s?action=%s&id=%s&category=%s" target="%s"' \
                       % (os.environ['SCRIPT_NAME'],ACTION_EDIT_HTTP_PERMISSIONS,id,category,WINDOW_DETAILS)
        html_string += 'onClick=popup("%s")>HTTP</a>&nbsp;\n' % (WINDOW_DETAILS)
        html_string += '<A href="%s?action=%s&id=%s&category=%s" target="%s"' \
                       % (os.environ['SCRIPT_NAME'],ACTION_EDIT_FTP_PERMISSIONS,id,category,WINDOW_DETAILS)
        html_string += 'onClick=popup("%s")>FTP</a>\n' % (WINDOW_DETAILS)
        if category == CATEGORY_GROUPS:
            html_string += '<a href="%s?action=%s&id=%s" target="%s"' \
                           % (os.environ['SCRIPT_NAME'],ACTION_EDIT_EXTENSIONS,id,WINDOW_DETAILS) 
            html_string += 'onClick=popup("%s")>%s</A>\n' % (WINDOW_DETAILS, _('Extensions'))
	#Add msn menu - for all categorys
        html_string += '<a href="%s?action=%s&id=%s&category=%s" target="%s"' \
                           % (os.environ['SCRIPT_NAME'],ACTION_EDIT_MSN,id,category,WINDOW_DETAILS) 
        html_string += 'onClick=popup("%s")>%s</A>\n' % (WINDOW_DETAILS, _('MSN'))
        # Add bandwidth limit for all categories
        html_string += '<a href="%s?action=%s&id=%s&category=%s" target="%s"' \
                           % (os.environ['SCRIPT_NAME'], ACTION_EDIT_BANDWIDTH, id, category, WINDOW_DETAILS)
        html_string += 'onClick=popup("%s")>%s</A>\n' % (WINDOW_DETAILS, _('Bandwidth limit'))
        html_string += '</td>\n'
	#End msn menu
        html_string += '<td><a href="%s?action=%s&id=%s&category=%s" target="%s"' \
                       % (os.environ['SCRIPT_NAME'],ACTION_DELETE,id,category,WINDOW_DETAILS)
	html_string += 'onClick=popup("%s")>%s</a></td>\n' % (WINDOW_DETAILS, _('delete'))
        html_string +=  '</tr>\n'
        i = i+1 
    html_string +=  '<tr><th colspan=%s align=left>&nbsp;</th>' % colspan_footer
    html_string += '<th colspan=2 align=center> <A href=%s?action=%s&category=%s target="%s"' \
                   % (os.environ['SCRIPT_NAME'], ACTION_CREATE,category,WINDOW_DETAILS)
    html_string += ' onClick=popup("%s")>%s</a>&nbsp;</th></tr>\n' % (WINDOW_DETAILS, create_new)
    html_string += '</table></center>'
    print html_string
