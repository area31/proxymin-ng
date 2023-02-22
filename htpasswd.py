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

import crypt
import random
import string
import os

import configparser

global htpasswd_file 
from globals import *

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH + CONFIG_FILE)

htpasswd_file = config.get("files","htpasswd_file")

def mkeSalt():
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    valid_chars = "abcdefghijklmnopqrstuvwxyz" + valid_chars
    valid_chars = "0123456789" + valid_chars
    valid_chars = "./" + valid_chars
    salt = ""
    for i in range(2):
        salt = random.choice(valid_chars) + salt
    return salt

def encrypt(pwd):
    salt = mkeSalt()
    return crypt.crypt(pwd, salt)

def reset():
    myfile = open(htpasswd_file, 'w')
    myfile.close

def getUserNames():
    myfile = create_or_read_file(htpasswd_file)
    lines = myfile.readlines()
    users = []
    for l in lines:
        if l != "\n":
            users.append(string.split(l,':')[0])
    myfile.close()
    return users

def getUsers():
    myfile = create_or_read_file(htpasswd_file)
    lines = myfile.readlines()
    users = []
    for l in lines:
        if l != "\n":
            users.append((string.split(l,':')[0],string.split(l,':')[1][:-1]))
    myfile.close()
    return users

def updateUser(username, password):
    delUser(username)
    addUser(username, password) 

def addUser(username, password):
    usernames = getUserNames()
    if username not in usernames:
        users = getUsers()
        users.append((username, password))
        users.sort()
        myfile = open(htpasswd_file, 'w')
        for l in users:
            myfile.write(l[0] + ":" + l[1] + "\n")
        # the original htpasswd from the apache group has an additional newline
        # at the end, so we do the same 
        myfile.write("\n")
        myfile.close()

def delUser(username):
    users = getUsers()
    for i in range(len(users)):
        if users[i][0] == username: 	
            del users[i]
            break 
    myfile = open(htpasswd_file, 'w')
    for l in users:
         myfile.write(l[0] + ":" + l[1] + "\n")
    # the original htpasswd from the apache group has an additional newline
    # at the end, so we do the same 
    myfile.write("\n")
    myfile.close()

def create_or_read_file(path):
    return os.fdopen(os.open(path, os.O_CREAT|os.O_RDONLY))
