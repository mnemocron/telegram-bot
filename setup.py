#!/usr/bin/python
#_*_ coding: utf-8 _*_

'''
@file 			setup.py
@author 		Simon Burkhardt - simonmartin.ch - github.com/mnemocron
@date 			2017.09.07
'''

CONF_DIRECTORY = '/etc/telegram-bot'

try:
	import errno					# error numbers
	import sys 						# argv
	import os 						# files, directories
	import requests					# requesting webpages
	import json 					# parsing API response and conf file
except Exception as e:
	print >> sys.stderr, 'Error importing modules'
	print >> sys.stderr, e
	sys.exit(1)

if ( len(sys.argv) < 2 ):
	print >> sys.stderr, 'No bot token provided.'
	print 'usage:'
	print '\tsudo ./setup.py [bot_token]'
	sys.exit(1)

bot_token = sys.argv[1]

try:
	os.mkdir(CONF_DIRECTORY)
except OSError as e:
	if (e[0] == errno.EACCES):
		print >> sys.stderr, 'You need root permissions to do this!'
		sys.exit(1)
	if (e[0] == errno.EEXIST):
		if os.path.exists(CONF_DIRECTORY + '/telegram-bot.conf'):
			print ('There is already a conf file present under: ' + CONF_DIRECTORY + '/telegram-bot.conf')
			sys.exit(1)

json_bot_conf = {}

requrl = 'https://api.telegram.org/bot' + bot_token + '/getMe'
response = requests.get(requrl)
if (response.status_code == 200):
	json_response = json.loads(response.text)
	if (json_response['ok'] == True):
		json_bot_conf['id'] 		= json_response['result']['id']
		json_bot_conf['first_name'] = json_response['result']['first_name']
		json_bot_conf['username']	= json_response['result']['username']
		json_bot_conf['token'] = str(bot_token)
		json_bot_conf['chats'] = []
		print json.dumps(json_bot_conf, indent=4)
else:
	json_response = json.loads(response.text)
	print str(json_response['error_code']) + ' - ' + json_response['description']

with open(CONF_DIRECTORY + '/telegram-bot.conf', 'w') as conf_file:
	json.dump(json_bot_conf, conf_file, indent=4)

print ('\nSuccessfully created conf file under:' + CONF_DIRECTORY + '/telegram-bot.conf')

os.popen('cp ./telegram-bot.py /usr/bin/telegram-bot')
os.popen('chmod 755 /usr/bin/telegram-bot')
