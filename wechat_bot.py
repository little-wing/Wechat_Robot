# -*- coding: utf-8 -*-
import sys
import time
from wxbot import *

class myWechatBot(WXBot):
	def handle_msg_all(self, msg):
		print msg
		for (k, v) in msg.items():
			print "%s => %s" % (k, v)
		#群聊 msg_type_id 为 3
		if msg['msg_type_id'] == 4:
			print "==================="
			print msg['user']['name']
#			self.send_msg(msg['user']['name'], msg['content']['data'])
			self.send_msg_by_uid("Message sent by uid!", msg['user']['id'])
			print "==================="

#		else:
#			self.send_msg('benyu_cn', 'good')
			
	def schedule(self):
		self.send_msg('benyu_cn', 'this is schedule')
		time.sleep(2)

def main():
	bot = myWechatBot()
	bot.DEBUG = True
	bot.run()
		
if __name__ == '__main__':
	main()