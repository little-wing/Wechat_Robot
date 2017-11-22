# -*- coding: utf-8 -*-
import sys
import time
import sqlite3
from wxbot import *

class myWechatBot(WXBot):

#	wechat_DB = 'D:\SQLite\DB_Files\wechatBotDB.db'

	def handle_msg_all(self, msg):
#		print msg
		for (k, v) in msg.items():
			print "%s => %s" % (k, v)
		# group msg_type_id = 3
		# contact msg_type_id = 4
		if msg['msg_type_id'] == 3:
			print "******************"
			print msg['user']['id']
			print "******************"
			# time_stamp is the primary key in chat_history
			time_stamp = time.time()
			current_date = time.strftime("%Y-%m-%d", time.localtime())
			current_time = time.strftime("%H:%M:%S", time.localtime())

			insert_value = (time_stamp, msg['user']['id'], current_date, current_time, msg['content']['data'])
#			print insert_value
			wechat_DB = 'D:\SQLite\DB_Files\wechatBotDB.db'
			conn = sqlite3.connect(wechat_DB)
			cur = conn.cursor()

			cur.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?)", insert_value)
			conn.commit()		
			conn.close()

#			print msg['user']['name']
#			self.send_msg(msg['user']['name'], msg['content']['data'])
#			self.send_msg_by_uid("群聊消息收到", msg['user']['id'])

#		else:
#			self.send_msg('benyu_cn', 'good')
			

def main():
	bot = myWechatBot()
	bot.DEBUG = True
	bot.run()
		
if __name__ == '__main__':
	main()