# -*- coding: utf-8 -*-
import sys
import re
import time
import sqlite3
from wxbot import *

class myWechatBot(WXBot):

	wechat_DB = 'D:\SQLite\DB_Files\wechatBotDB.db'
	def handle_msg_all(self, msg):
#		print msg
		print "=========================================================================="
		for (k, v) in msg.items():
			print "%s => %s" % (k, v)
		# group msg_type_id = 3
#		if msg['msg_type_id'] == 3:
		# contact msg_type_id = 4
		if msg['msg_type_id'] == 4:
			print "******************"
			print msg['user']['id']
			print msg['user']['name']
			print "******************"
			
			# Connect DB. 
#			wechat_DB = 'D:\SQLite\DB_Files\wechatBotDB.db'
			conn = sqlite3.connect(self.wechat_DB)
			cur = conn.cursor()
			
			# Collect user id. Comment this block out when collect user data is done.
			insert_userData = (msg['user']['id'], msg['user']['name'])
			cur.execute("INSERT OR IGNORE INTO id_list VALUES (?, ?)", insert_userData)
			
			# Insert data into DB
			# time_stamp is the primary key in chat_history
			if msg['user']['id'] == '@fb7d161360c0c80b0aa8d0f5e2dd2a07':
				time_stamp = time.time()
				current_date = time.strftime("%Y-%m-%d", time.localtime())	
				current_time = time.strftime("%H:%M:%S", time.localtime())
#				insert_chatHistory = (time_stamp, msg['user']['id'], current_date, current_time, msg['content']['data'])
#				cur.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?)", insert_chatHistory)
				cur.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?)", (time_stamp, msg['user']['id'], current_date, current_time, msg['content']['data']))
				conn.commit()		
				
				
			if msg['content']['data'] == 'today':
				current_date = time.strftime("%Y-%m-%d", time.localtime())
				teacher_instruction = cur.execute("SELECT CONTENT FROM chat_history WHERE DATE=?", (current_date,))
				for line in teacher_instruction:
					print line

			conn.close()
#			print msg['user']['name']
#			self.send_msg(msg['user']['name'], msg['content']['data'])
#			self.send_msg_by_uid("群聊消息收到", msg['user']['id'])

			

def main():
	bot = myWechatBot()
	bot.DEBUG = True
	bot.run()
		
if __name__ == '__main__':
	main()
