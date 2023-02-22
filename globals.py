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

TRUE = (1 == 1)
FALSE = (0 == 1)

#PROGRAM
PROGRAM_VERSION = '1.0.0'
PROGRAM_NAME = 'Proxy Admin'
PROJECT_HOMEPAGE = 'https://www.vipnix.com.br'
CONTACT_EMAIL = "mail"

#FILES
CONFIG_FILE_PATH = ''
CONFIG_FILE = 'proxymin.conf'
CSS_FILE = 'css/css.txt'

#JAVA SCRIPT
JS_HEIGHT_DEFAULT = 300
JS_WIDTH_DEFAULT = 300
PAGE_HELP_HEIGHT = 600
PAGE_HELP_WIDTH = 800
PAGE_INFO_HEIGHT = 600
PAGE_INFO_WIDTH = 700

#HTTP/FTP/EXTENSION DEFAULTS
MINIMUM_URL_ROWS = 4
ADDITIONAL_URL_ROWS = 8

#IMAGES
IMAGE_SCRIPT = 'images.py'
IMAGE_DIR = 'images/'
IMAGE_GET_VARIABLE = 'img'
IMAGE_BALL_RED = 'ball_red'
IMAGE_BALL_GREEN = 'ball_green'
IMAGE_BALL_RED_FILE = '/proxymin/images/ball_red.gif'
IMAGE_BALL_GREEN_FILE = '/proxymin/images/ball_green.gif'

#ACTIONS (for use as GET-vars)
ACTION_SHOW_MAIN = 'show_main'
ACTION_CREATE = 'create'
ACTION_DELETE = 'delete'
ACTION_EDIT = 'edit'
ACTION_SAVE_CREATE = 'save_create'
ACTION_SAVE_DELETE = 'save_delete'
ACTION_SAVE_EDIT = 'save_edit'
ACTION_EDIT_HTTP_PERMISSIONS = 'edit_http_permissions'
ACTION_EDIT_FTP_PERMISSIONS = 'edit_ftp_permissions'
ACTION_EDIT_EXTENSIONS = 'edit_extensions'
ACTION_EDIT_MSN = 'edit_msn'
ACTION_EDIT_BANDWIDTH = 'edit_bandwidth'
ACTION_SAVE_HTTP_PERMISSIONS = 'save_http_permissions'
ACTION_SAVE_FTP_PERMISSIONS = 'save_ftp_permissions'
ACTION_SAVE_EXTENSIONS = 'save_extensions'
ACTION_SAVE_MSN = 'save_msn'
ACTION_SAVE_BANDWIDTH = 'save_bandwidth'
ACTION_DISPLAY_HELP = 'display_help'
ACTION_DISPLAY_INFO = 'display_info'

#PREDEFINED STRINGS
WINDOW_DETAILS = 'window_details'
WINDOW_INFO = 'window_info'
WINDOW_HELP = 'window_help'
PASSWORD_UNCHANGED = '********'
CATEGORY_USERS = 'users'
CATEGORY_HOSTS = 'hosts'
CATEGORY_GROUPS = 'groups'
PROTOCOL_HTTP = 'http'
PROTOCOL_FTP = 'ftp'
SSL_FROM_GROUP = 'ssl_from_group'
SSL_ENABLED = 'ssl_enabled'
SSL_DISABLED = 'ssl_disabled'
MSN_FROM_GROUP= 'msn_from_group'
MSN_ENABLED = 'msn_enabled'
MSN_DISABLED = 'msn_disabled'

#MISC
SQUID_HOMEPAGE = 'http://www.squid-cache.org/'
SQUID_ACL_URL = 'http://www.squid-cache.org/Doc/FAQ/FAQ-10.html'
PYTHON_HOMEPAGE = 'http://www.python.org'
GPL_URL = 'http://www.gnu.org/copyleft/gpl.html'
ALLOWED = 'allowed'
DENIED = 'denied'
NONE = 'none'
ENABLED = 'enabled'
DISABLED = 'disabled'
