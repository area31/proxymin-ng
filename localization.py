# -*- coding: UTF-8 -*-
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

from globals import *

def umlaut_encode(to_encode):
    encoded = ''
    for char in to_encode:
        if(char == 'ä'):
            encoded = encoded + '&auml;'
        elif(char == 'Ä'):
            encoded = encoded + '&Auml;'
        elif(char == 'ö'):
            encoded = encoded + '&ouml;'
        elif(char == 'Ö'):
            encoded = encoded + '&Ouml;'
        elif(char == 'ü'):
            encoded = encoded + '&uuml;'
        elif(char == 'Ü'):
            encoded = encoded + '&Uuml;'
        elif(char == 'ß'):
            encoded = encoded + '&suml;'
        else:
            encoded = encoded + char
    return encoded

def _(to_translate):
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE_PATH + "proxymin.conf")
    lang_dir = config.get("files","lang_dir")
    lang = config.get("parameters","language")
    filename = lang_dir + 'lang_' + lang
    
    if(os.access(filename,os.R_OK)):
        file = open(filename)       
    else:
        return to_translate
    
    for line in file.readlines():
        # ignore comments
        if(line[0] == '#'):
            continue
        if(string.split(string.split(line, '::')[0], "'")[1] == to_translate):
            file.close()
            return umlaut_encode(string.split(string.split(line, '::')[1], "'")[1])
        
    return to_translate
    file.close()
