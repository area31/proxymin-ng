#!/usr/bin/python
#
# Script que insere uma lista de sites ou apenas um unico site no database do proxymin. 
# Deve-se copiar esse arquivo para o diretorio raiz do proxymin para executar
#
#


import dbaccess
import permissions
import objectiterator

from globals import *

#Crir objeto iterator, usando a classe objectierator.py, setando a categoria GROUPS (possiveis(GROUPS, HOSTS, USERS)
iterator = objectiterator.ObjectIterator(CATEGORY_GROUPS)
#Objeto que vai utilizar o ID como o nome do grupo (Grupo-ID)
object = iterator.get_object('Sinistro-Regulagem')

#Imprimir todas URLS setadas do grupo acima
print object.get_http_permissions().get_url_list()

#Inserir URL ao Grupo acima
#Vai inserir as urls, adicionando as ja existentes, nao grava urls repetidas

##############################Inserindo somente uma url:#############################
##object.get_http_permissions().add_url('www.foi.com.br')
###############################################################################

########################### #Inserindo varias urls: ##############################
#Abrir arquivo
filehandleit=open('/root/lista-g.txt', 'r')
#Ler cada linha
for line in filehandleit:
	#Remover os ultimos 2 caracteres de line (\r e \n)
	line = line[:-1]
	#Inserir o objeto dentro do proxymin, usando line
	object.get_http_permissions().add_url(line)
#Fechar handle
filehandleit.close()
##################################################################################


#Imprimir novamente todas urls setadas
print object.get_http_permissions().get_url_list()


#Atualizar arquivo com as alteracoes efetuadas:
iterator.update_object(object)

