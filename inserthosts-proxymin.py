import os
import string
import sys

import configparser

import dbaccess
import gui_misc
import gui_object_details
import objectiterator
from globals import *
from localization import _

#Criar objeto iterator, usando a classe objectierator.py, setando a categoria GROUPS (possiveis(GROUPS, HOSTS, USERS)
iterator = objectiterator.ObjectIterator(CATEGORY_HOSTS)

# Pegar hosts da arvore do AD
#sys.exec("net rpc user -U proxyinternet%Proxymegapass26910 -S scbdc01")
#userlist = os.popen("net rpc user -U proxyinternet%Proxymegapass26910 -S scbdc01 >/tmp/userlist.txt")

#Ler arquivo com hosts e inserir na base
#Abrir arquivo
filehandleit=open('/tmp/hostlist.txt', 'r')
#Ler cada linha
for host in filehandleit:
        #Remover os ultimos 2 caracteres de line (\r e \n)
        host = host[:-1]
        #Se host existir, abortar
        if iterator.get_object(host):
            print("Host " + host + " já existe na base de dados. Ignorando.")
            continue
        category='hosts'
        description=''
        group='Liberado'
        active='checked'
        gui_object_details.save_input_data(category, host, description, group, active)
        #iterator.add_object(host)
        #object = iterator.get_object(host)
        #object.set_description('')
        #object.set_group('Bloqueado')
        #object.enable()
        #iterator.update_object(object)
        print("Host " + host + " inserido")

#Commit

