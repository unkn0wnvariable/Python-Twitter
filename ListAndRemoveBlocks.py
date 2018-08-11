from __future__ import print_function
from MyTwitterFunctions import *

blocks = twitter.list_blocks(include_entities='False', skip_status='True')

if len(blocks['users']) > 0:
	for user in blocks['users']:
		print('Blocked user: ' + user['name'])

	makeChanges = ''
	while not makeChanges == 'y' and not makeChanges == 'n':
		makeChanges = input('Do you want to remove these blocks? (y/n) ')

	if makeChanges == 'y':
		for user in blocks['users']:
			print('Unblocking user: ' + user['name'])
			twitter.destroy_block(user_id=user['id'])
else:
	print('Not blocking anyone')
