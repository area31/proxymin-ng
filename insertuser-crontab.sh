#!/bin/bash

# Script para criar usuários no proxymin
#*/3 * * * *     root    /srv/www/htdocs/proxymin/insertuser-crontab.sh

MACHINE_AD="servidor"
USER_AD="vipnix"
PASSWORD_AD="123"

#########################################################

WINBIND_CHECK_SERVICE="1"
WINBIND_INIT="/etc/init.d/winbind"
WINBIND_PORTS_TCP=""
WINBIND_PORTS_UDP=""
WINBIND_USER="root"
WINBIND_COMMAND="winbind"
WINBIND_SERVICE_NAME="winbind"

WINBIND_JOIN_DOMAIN="VIPNIX"
WINBIND_JOIN_USER="vipnix"
WINBIND_JOIN_PASSWD="123"


WINBIND_CHECK_JOINED=$(wbinfo -a ${WINBIND_JOIN_DOMAIN}\\${WINBIND_JOIN_USER}%${WINBIND_JOIN_PASSWD}|grep -wi succeeded|wc -l)
if [ "${WINBIND_CHECK_JOINED}" -eq 0 ]; then
        echo -e "$(date) - Problema de ingresso no dominio, reiniciando ${WINBIND_SERVICE_NAME}...\n" 
        ${WINBIND_INIT} stop 2>&1
        ${WINBIND_INIT} start
        sleep 3
        squid -k reconfigure
fi
#########################################################

# Geração de lista de usuários do AD
net rpc user -S ${MACHINE_AD} -U${USER_AD}%${PASSWORD_AD} |sort|uniq | tr [A-Z] [a-z] |grep -iv support_ | grep -iv nt_status_ | grep -iv '$duplicate-'| grep -iv 'user_system_' |grep -iv 'iusr_' |grep -iv 'iwam_' |grep -iv 'did you forget to run kinit' |grep -iv 'called name not present' |grep -iv 'session request to' |grep -iv ' ' > /tmp/userlist_temp.txt
sed 's/^/VIPNIX\\/' /tmp/userlist_temp.txt > /tmp/userlist.txt

# Geração de lista de usuários do LDAP
#ldapsearch -h localhost -p 389 -b "ou=People,dc=vipnix,dc=com,dc=br" -D "cn=admin,dc=vipnix,dc=com,dc=br"  -w senha | grep givenName | sed s,"givenName: ",'',g | sort | uniq | tr [A-Z] [a-z] > /tmp/userlist.txt

if [ $? -eq 0 ]; then
	cd /srv/www/htdocs/proxymin
	/usr/bin/python /srv/www/htdocs/proxymin/insertusers-proxymin.py
        echo "Sucesso.."
else
        echo "Erro ao criar lista de usuarios. Abortando." 
fi
