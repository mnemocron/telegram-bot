#!/usr/bin/python3
#_*_ coding: utf-8 _*_

'''
@file 			telegram-bot.py
@author 		Simon Burkhardt - simonmartin.ch - github.com/mnemocron
@date 			2017.09.10
'''

CONF_DIRECTORY = '/etc/telegram-bot'

try:
	import errno					# error numbers
	import sys 						# argv
	import os 						# files, directories
	import requests					# requesting webpages
	import json 					# parsing API response and conf file
	import optparse					# argument parser
	import select					# stdin input
except Exception as e:
	sys.stderr.write('Error importing modules')
	sys.stderr.write(e)
	sys.exit(1)

# reload(sys)
# sys.setdefaultencoding('utf-8')

parser = optparse.OptionParser('telegram-bot')
parser.add_option('-u', '-c', '--user', '--chat', 	dest='chat', 		type='string', help='specify the recipent')
parser.add_option('-t', '--text',					dest='text', 		type='string', help='specify the text to be sent')
parser.add_option('-s', '--stdin', 					dest='stdin', 			action='store_true', 	help='[optional] Use piped text from stdin instead of -t \"text\"')
parser.add_option('-p', '--parsing', 				dest='parsemode', 	type='string', help='[optional] specify the encoding type [markdown|html]')
parser.add_option('--disable-preview', 				dest='disable_prev', 	action='store_true', 	help='[optional] Disables link previews for links in this message.')
parser.add_option('--disable-notification', 		dest='disable_notif', 	action='store_true', 	help='[optional] Sends the message silently. Users will receive a notification with no sound.')
(opts, args) = parser.parse_args()

if ( opts.chat is None ):
	parser.print_help()
	sys.exit(1)

if ( opts.text is None and opts.stdin is None ):
	sys.stderr.write('Please specify something to send (--text or --stdin).')
	sys.exit(1)

try:
	# open configuration file
	try:
		with open(CONF_DIRECTORY + '/telegram-bot.conf', 'r') as conf_file:
			json_conf = json.loads(conf_file.read())
	except IOError as e:
		if (e[0] == 2) :
			sys.stderr.write('No conf file found in ' + CONF_DIRECTORY)
			sys.exit(1)
		sys.stderr.write('Error opening configuration file')
		sys.exit(1)

	chat_id = []
	for user in json_conf['chats']:
		if (opts.chat.replace('@', '') == user['username']):
			chat_id = user['id']

	if (len(str(chat_id)) < 3):
		sys.stderr.write('User not found: ' + opts.chat)
		sys.exit(1)

	message_text = ''
	if (opts.stdin is True):
		if ( select.select([sys.stdin,],[],[],0.0)[0] ) :
			for line in sys.stdin:
				message_text += line

	if (opts.text is not None):
		message_text += opts.text

	parse_mode = ''
	if (opts.parsemode is not None):
		if (opts.parsemode.lower() == 'html'):
			parse_mode = 'html'
		elif (opts.parsemode.lower() == 'markdown'):
			parse_mode = 'markdown'
		else:
			sys.stderr.write('Unsupported parse mode: ' + opts.parsemode)
			sys.exit(1)

	requrl = 'https://api.telegram.org/bot' + str(json_conf['token']) + '/sendMessage'
	payload = {
		'chat_id' 		: str(chat_id).encode('utf-8'),
		'text' 			: message_text.encode('latin1').decode('unicode-escape').encode('utf-8')
	}
    # need to decode escaped sequences for \n
    # https://stackoverflow.com/a/14820462

	if (len(parse_mode) > 3):
		payload['parse_mode'] = parse_mode.encode('utf-8')

	if (opts.disable_notif is True):
		payload['disable_notification'] = True

	if (opts.disable_prev is True):
		payload['disable_web_page_preview'] = True

	response = requests.post(requrl, data=payload)

	if (response.status_code != 200):
		print (response.text)

except KeyboardInterrupt:
	print ("")
	sys.exit(0)

