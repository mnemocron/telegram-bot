#!/usr/bin/python
#_*_ coding: utf-8 _*_

'''
@file 			add-new-user.py
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

# check root privileges
try:
	os.mkdir(CONF_DIRECTORY + '/test')
	os.rmdir(CONF_DIRECTORY + '/test')
except OSError as e:
	if (e[0] == errno.EACCES):
		print >> sys.stderr, 'You need root permissions to do this!'
		sys.exit(1)

try:
	with open(CONF_DIRECTORY + '/telegram-bot.conf', 'r') as conf_file:
		json_conf_old = json.loads(conf_file.read())
except IOError as e:
	if (e[0] == 2) :
		print >> sys.stderr, 'No conf file found in ' + CONF_DIRECTORY
		sys.exit(1)
	print >> sys.stderr, 'Error opening configuration file'
	sys.exit(1)

# create new configuration object
json_conf_new = json_conf_old

'''
{
    "ok": true, 
    "result": [
        {
            "message": {
                "date": 1504791255, 
                "text": "hello world!", 
                "from": {
                    "username": "***", 
                    "first_name": "***", 
                    "last_name": "***", 
                    "is_bot": false, 
                    "language_code": "en-GB", 
                    "id": ***057***
                }, 
                "message_id": 1135, 
                "chat": {
                    "username": "***", 
                    "first_name": "***", 
                    "last_name": "***", 
                    "type": "private", 
                    "id": ***057***
                }
            }, 
            "update_id": **195****
        }
    ]
}

'''

# yes-no query function
def query_yes_no(question, default='no'):
	valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}
	if default is None:
		prompt = ' [y/n] '
	elif default == 'yes':
		prompt = ' [Y/n] '
	elif default == 'no':
		prompt = ' [y/N] '
	else:
		raise ValueError('invalid default answer: \"%s\"' % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write('Please respond with \"yes\" or \"no\" (or \"y\" or \"n\").\n')

# new user add function
# takes a json-object as argument
def add_new(user):
	if(user['message']['chat']['type'] == 'group'):
		add_new = query_yes_no('Do you want to add group \"' 
			+ user['message']['chat']['title'] + '\" ?', 'no')
	else:
		add_new = query_yes_no('Do you want to add user \"' 
			+ user['message']['from']['username'] + '\" ('
			+ user['message']['from']['first_name'] + ' ' + user['message']['from']['last_name']
			+ ') ?', 'no')
	if add_new is True:
		if (user['message']['chat']['type'] == 'group'):
			json_conf_new['chats'].append({})
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['username'] 		= user['message']['chat']['title']
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['first_name'] 	= ''
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['last_name'] 	= ''
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['id']			= user['message']['chat']['id']
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['type']			= 'group'
			print '[info] - added new group: ' + user['message']['chat']['title']
		else:
			json_conf_new['chats'].append({})
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['username'] 		= user['message']['from']['username']
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['first_name'] 	= user['message']['from']['first_name']
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['last_name'] 	= user['message']['from']['last_name']
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['id']			= user['message']['from']['id']
			json_conf_new['chats'][len(json_conf_new['chats']) -1]['type']			= 'private'
			print '[info] - added new chat: ' + user['message']['from']['username']

# looking up new messages
requrl = 'https://api.telegram.org/bot' + str(json_conf_old['token']) + '/getUpdates'
response = requests.get(requrl)
if (response.status_code == 200):
	json_response = json.loads(response.text)
	if (json_response['ok'] == True):
		for update in json_response['result']:
			if (update['message']['chat']['type'] == 'group'):
				if ( (update['message']['chat']['title'] not in json.dumps(json_conf_old['chats'])) and 
					(update['message']['chat']['title'] not in json.dumps(json_conf_new['chats'])) ):
					# print update['message']['chat']['title'] + ' not in ' + json.dumps(json_conf_new['chats'])
					add_new(update)
				else :
					print('[info] - group \"' + update['message']['chat']['title'] + '\" is already added.')
			elif 'text' in update['message']:
				if ('add me' in update['message']['text'].lower() ):
					if ( (update['message']['from']['username'] not in json.dumps(json_conf_old['chats'])) and
						(update['message']['from']['username'] not in json.dumps(json_conf_new['chats'])) ):
						add_new(update)
					else :
						print('[info] - user \"' + update['message']['from']['username'] + '\" is already added.')

else:
	json_response = json.loads(response.text)
	print str(json_response['error_code']) + ' - ' + json_response['description']

print ('[info] - writing changes to ' + CONF_DIRECTORY + '/telegram-bot.conf')
with open(CONF_DIRECTORY + '/telegram-bot.conf', 'w') as conf_file:
	json.dump(json_conf_new, conf_file, indent=4)
