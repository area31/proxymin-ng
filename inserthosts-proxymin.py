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

# Criar objeto iterator, usando a classe objectiterator.py, setando a categoria HOSTS
iterator = objectiterator.ObjectIterator(CATEGORY_HOSTS)

# Abrir arquivo com hosts e inserir na base
# Verificar se o arquivo existe antes de abri-lo
if os.path.exists('/tmp/hostlist.txt'):
    # Abrir arquivo
    filehandleit = open('/tmp/hostlist.txt', 'r')
    # Ler cada linha
    for host in filehandleit:
        # Remover os últimos 2 caracteres de line (\r e \n)
        host = host[:-1]
        # Verificar se o host já existe no banco de dados
        if iterator.get_object(host):
            print("Host " + host + " já existe no banco de dados.")
        else:
            category = 'hosts'
            description = ''
            group = 'Liberado'
            active = 'checked'
            gui_object_details.save_input_data(category, host, description, group, active)
            print("Host " + host + " inserido.")
    # Fechar arquivo
    filehandleit.close()
else:
    print("Arquivo /tmp/hostlist.txt não encontrado.")

