#!/usr/bin/python
#
# Script que sincroniza usuarios do AD com o proxymin
#

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

#Cria objeto iterator, usando a classe objectierator.py, setando a categoria GROUPS (possiveis(GROUPS, HOSTS, USERS)
iterator = objectiterator.ObjectIterator(CATEGORY_USERS)

#Objeto que vai utilizar o ID como o nome do grupo (Grupo-ID)
#object = iterator.get_object('Bloqueado')
#object = iterator.get_object('testando')

# Pegar usuarios da arvore do AD
#sys.exec("net rpc user -U proxyinternet%Proxymegapass26910 -S scbdc01")
#userlist = os.popen("net rpc user -U proxyinternet%Proxymegapass26910 -S scbdc01 >/tmp/userlist.txt")

# Verificar se o arquivo de usuários existe
if os.path.exists('/tmp/userlist.txt'):
    # Ler arquivo com users e inserir na base
    # Abrir arquivo
    filehandleit = open('/tmp/userlist.txt', 'r')
    # Ler cada linha
    for usuario in filehandleit:
        # Remover os ultimos 2 caracteres de line (\r e \n)
        usuario = usuario[:-1]
        # Se usuario existir, abortar
        if not(iterator.get_object(usuario)):
            category = 'users'
            description = ''
            group = 'Padrao'
            active = 'checked'
            gui_object_details.save_input_data(category, usuario, description, group, active)
            print("Usuario " + usuario + " inserido")

else:
    print("Arquivo de usuários não encontrado")

