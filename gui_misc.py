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

import os
import string

import ConfigParser

import dbaccess
import objectiterator
from globals import *
from localization import _

def print_html_head(title=PROGRAM_NAME):
    print '<html><head><title>%s</title>' % title
    print_encoding()
    print_java_scripts()
    print_css()
    print '</head>'

def print_java_scripts():

    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE_PATH + CONFIG_FILE)
    
    values = {'default_width':JS_WIDTH_DEFAULT,
              'default_height':JS_HEIGHT_DEFAULT,
              'maximum_height':int(config.get("parameters","maximum_popup_height"))}
    template = """
<SCRIPT LANGUAGE="JavaScript">
<!--
function popup(window_name,width,height)
{
  if(!width) width = %(default_width)i;
  if(!height) height = %(default_height)i;
  var attributes = "WIDTH=" + width + ",HEIGHT=" + height + ",location=no,dependent=yes,resizable=yes,scrollbars=yes,menubar=no";
  var new_window=window.open('',window_name, attributes);
  new_window.focus();
}

function go(url)
{
  if (url=="nothing") {return;}
  else { 
    window.location.href=url;
  }
}

// the next two scripts are used with written permission from Mark 'Tarquin' Wilton-Jones
// for copyright details see: http://www.howtocreate.co.uk/jslibs/termsOfUse.html
function getRefToDivMod( divID, oDoc ) {
	if( !oDoc ) { oDoc = document; }
	if( document.layers ) {
		if( oDoc.layers[divID] ) { return oDoc.layers[divID]; } else {
			for( var x = 0, y; !y && x < oDoc.layers.length; x++ ) {
				y = getRefToDivNest(divID,oDoc.layers[x].document); }
			return y; } }
	if( document.getElementById ) { return oDoc.getElementById(divID); }
	if( document.all ) { return oDoc.all[divID]; }
	return document[divID];
}

function resizeWinTo( idOfDiv ) {
    var oH = getRefToDivMod( idOfDiv ); if( !oH ) { return false; }
    var oW = oH.clip ? oH.clip.width : oH.offsetWidth;
    var oH = oH.clip ? oH.clip.height : oH.offsetHeight; if( !oH ) { return false; }
    var x = window; x.resizeTo( oW + 200, oH + 200 );
    var myW = 0, myH = 0, d = x.document.documentElement, b = x.document.body;
    if( x.innerWidth ) { myW = x.innerWidth; myH = x.innerHeight; }
    else if( d && d.clientWidth ) { myW = d.clientWidth; myH = d.clientHeight; }
    else if( b && b.clientWidth ) { myW = b.clientWidth; myH = b.clientHeight; }
    if( window.opera && !document.childNodes ) { myW += 16; }
    var height = oH + ( (oH + 200 ) - myH );
    //extra height check added by Clemens Hermann
    if (height > %(maximum_height)i)
    {
        height = %(maximum_height)i;
    }
    x.resizeTo( oW + ( ( oW + 650 ) - myW ), 500 );
}
//-->
</SCRIPT>"""
    print template % values

def print_css():
    css_file= open(CSS_FILE,'r')
    for line in css_file.readlines():
        print line,
    css_file.close()

def is_alphanum(input):
    valid_chars = string.letters + string.digits + "_" + "-" + "." + "\\"
    for char in input:
        if char not in valid_chars:
            return FALSE
    return TRUE

def is_ip(input):
    valid_chars = string.digits + "."
    for char in input:
        if char not in valid_chars:
            return 0
    segments = string.split(input, '.')
    if len(segments) != 4:
        return 0
    for segment in segments:
        if(string.atoi(segment) > 255):
            return 0    
    return 1

def print_popup_head(colspan, title='', error_message = ''):   
    print '<HTML><HEAD><TITLE>%s</TITLE>' % (title)    
    print_encoding()
    print_css()
    print_java_scripts()
    print '</HEAD><BODY>'
    print '<div style="position:absolute;left:0px;top:0px;width:0px;" id="resize_div">'
    print '<center><table border=0 CELLSPACING=2 CELLPADDING=3>\n'
    print '<tr class="titlebar"><td class="title" colspan=%s><nobr>%s</nobr></td></tr>' % (colspan, title)
    if(error_message != ''):  
        print '<tr><td colspan="%s" class="statusbar">' % (colspan)
        print '<b>%s</b></td></tr>' % (error_message)
    print '<tr><td colspan="%s">&nbsp;</td><tr>' % (colspan)

def print_footer():
    # read the configuration file
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE_PATH + CONFIG_FILE)
    
    html_string = '<center><font class="footer">'
    html_string += '%s<br>\n' % config.get("data","company_name")
    html_string += 'powered by <a href="%s" TARGET="blank">%s</a>\n' % (PROJECT_HOMEPAGE, PROGRAM_NAME)
    html_string += '</font></center>\n'
    html_string += '</body></html>\n'
    print html_string

def print_encoding():
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE_PATH + CONFIG_FILE)
    print '<meta http-equiv="Content-Type" content="text/html; charset=%s">\n' % config.get("parameters", "encoding")

def group_selector(default_group = ''):
    dba = dbaccess.DBAccess()
    html_string = ''
    html_string += '<select name="group">\n'
    for group in dba.get_group_list():
        html_string += '<OPTION value=%s' % (group)
        if group == default_group:
            html_string += ' SELECTED'
        html_string += '>%s</option>' % group
        html_string += '</option>\n'
    html_string += '</select>'
    return html_string

class RowFormat:
    def __init__(self):
        self.row_class = 'odd'
    def get_next_row_class(self):
        if(self.row_class == 'odd'):
            self.row_class = 'even'
        else:
            self.row_class = 'odd'
        return self.row_class
