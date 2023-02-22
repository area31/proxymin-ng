#!/usr/bin/env python

from poplib import POP3
import sys


#POP server against which we authenticate
server="10.0.0.2"
domain="@vipnix.com.br"
#Port number for POP server. Usually 110
port=110


#Below here you shouldn't need to edit anything

while 1:

        #Read user and password from stdin, remove the newline, split at the space
        #and assign to the user and password variables

        line=sys.stdin.readline()[:-1]
        [user,password]=line.split(' ')

        # Append @domain to username
        user=user+domain
        #Connect to the POP server

        p=POP3(server,port)

        #Try to authenticate. If it doesn't work, it throws an exception

        try:
                p.user(user)
                p.pass_(password)
        except:

                #If it threw an exception, log in cache.log the ayth booboo
                sys.stderr.write("ERR authenticating %s\n"%user)
                #Then deny access
                sys.stdout.write("ERR\n")
                #IMPORTANT!!!!!!!!!!!! Flush stdout
                sys.stdout.flush()
                continue

        #If it didn't throw exceptions, that means it authenticated

        #Log success to cache.log
        sys.stderr.write("OK authenticated %s\n"%user)
        #Then allow access
        sys.stdout.write("OK\n")
        sys.stdout.flush()

