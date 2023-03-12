#!/usr/bin/python3
#
# Script que insere uma lista de sites ou apenas um unico site no database do proxymin.
# Deve-se copiar esse arquivo para o diretorio raiz do proxymin para executar
#

import sys
import os

import dbaccess
import permissions
import objectiterator

from globals import *

# Verifica se um argumento foi passado para o script
if len(sys.argv) < 2:
    print("Uso: python3 insertsites-proxymin.py <nome_do_grupo>")
    sys.exit(1)

# Obtém o nome do grupo a partir do argumento
group_name = sys.argv[1]

# Cria objeto iterator, usando a classe objectiterator.py, setando a categoria GROUPS (possiveis(GROUPS, HOSTS, USERS)
iterator = objectiterator.ObjectIterator(CATEGORY_GROUPS)

# Obtém o objeto do grupo especificado
group_object = iterator.get_object(group_name)

# Verifica se o grupo existe
if not group_object:
    print(f"Erro: o grupo '{group_name}' não existe.")
    sys.exit(1)

# Imprime todas URLS setadas do grupo acima
print(group_object.get_http_permissions().get_url_list())

# Inserir URL ao Grupo acima
# Vai inserir as urls, adicionando as ja existentes, nao grava urls repetidas

##############################Inserindo somente uma url:#############################
##group_object.get_http_permissions().add_url('www.foi.com.br')
###############################################################################

########################### #Inserindo varias urls: ##############################
# Abrir arquivo
if os.path.exists('/tmp/lista-g.txt'):
    filehandleit = open('/tmp/lista-g.txt', 'r')
    # Ler cada linha
    for line in filehandleit:
        # Remover os ultimos 2 caracteres de line (\r e \n)
        line = line[:-1]
        # Inserir o objeto dentro do proxymin, usando line
        group_object.get_http_permissions().add_url(line)
    # Fechar handle
    filehandleit.close()
    ##################################################################################
    
    
    # Imprime novamente todas urls setadas
    print(group_object.get_http_permissions().get_url_list())
    
    # Atualizar arquivo com as alteracoes efetuadas:
    iterator.update_object(group_object)
    
else:
    print("Arquivo /tmp/lista-g.txt não encontrado.")
