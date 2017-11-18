# -*- coding: utf-8 -*-
import sys
from wxbot import WXBot

class myWechatBot(WXBot):
	def handle_msg_all(self, msg):
		if msg['msg_type_id'] == 5:
			self.send_msg(msg['user_name'], 'hi')
		
if __name__ == '__main__':
	bot = myWechatBot()
	bot.run()