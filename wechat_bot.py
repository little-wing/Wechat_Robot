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
		# 群聊 msg_type_id 为 3
		if msg['msg_type_id'] == 4:
			print "==================="
#			conn = sqlite3.connect('D:\SQLite\DB_Files\wechatBotDB.db')

			# time_stamp is the primary key in chat_history
			time_stamp = time.time()
			current_date = time.strftime("%Y-%m-%d", time.localtime())
			current_time = time.strftime("%H:%M:%S", time.localtime())
#			insert_value = '(' + time_stamp + ', ' + msg['user']['id'] + ', ' + current_date + ', ' + current_time + ', ' + msg['content']['data'] + '),'
			insert_value = (time_stamp, msg['user']['id'], current_date, current_time, msg['content']['data'])
#			print insert_value
			wechat_DB = 'D:\SQLite\DB_Files\wechatBotDB.db'
			conn = sqlite3.connect(wechat_DB)
			cur = conn.cursor()
#			cur.execute("INSERT INTO wechat_history VALUES (2, '@fb7d161360c0c80b0aa8d0f5e2dd2a07', '2017-11-20 10:12:28', 'zzttrrss')")	
#			cur.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?)", insert_value)
#			cur.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?)", (1511182293.263, u'@55673322c6d1d45a4381f4484573187868dacab3744a346b3afdfb69344ed887', u'2017-11-20', u'20:51:33', u'zzzzxxx'))
			cur.execute("INSERT INTO chat_history VALUES (1511182293.263, '55673322c6d1d45a4381f4484573187868dacab3744a346b3afdfb6934d887', '2017-11-20', '20:51:33', 'zzzzxxx')")
			conn.commit()
			result = cur.execute("select * from chat_history")
			for row in result:
				print row
				
			conn.close()

#			print msg['user']['name']
#			self.send_msg(msg['user']['name'], msg['content']['data'])
#			self.send_msg_by_uid("Message sent by uid!", msg['user']['id'])
			print "==================="

#		else:
#			self.send_msg('benyu_cn', 'good')
			

def main():
	bot = myWechatBot()
	bot.DEBUG = True
	bot.run()
		
if __name__ == '__main__':
	main()