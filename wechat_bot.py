# -*- coding: utf-8 -*-
import sys
import re
import time
import sqlite3
import datetime
from wxbot import *

class myWechatBot(WXBot):

#	wechat_DB = 'D:\SQLite\DB_Files\wechatBotDB.db'
	wechat_DB = './wechatBotDB.db'
	
	def query_teacher_instruction(self, query_date):
		conn = sqlite3.connect(self.wechat_DB)
		cur = conn.cursor()
		teacher_instruction = cur.execute("SELECT TIME, CONTENT FROM chat_history WHERE DATE=?", (query_date,))
		output_str = ""
		for line in teacher_instruction:
			output_str = output_str + line[0] + '\n' + line[1] + '\n\n'	
		self.send_msg_by_uid(output_str, msg['user']['id'])
		conn.close()	
	
	def handle_msg_all(self, msg):
		print "=========================================================================="
		print msg
		for (k, v) in msg.items():
			print "%s => %s" % (k, v)
			
		# group msg_type_id = 3, contact msg_type_id = 4
		if msg['msg_type_id'] == 3:
#		if msg['msg_type_id'] == 4:
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
			#if msg['user']['id'] == '@fb7d161360c0c80b0aa8d0f5e2dd2a07':
			time_stamp = time.time()
			current_date = time.strftime("%Y-%m-%d", time.localtime())	
			current_time = time.strftime("%H:%M:%S", time.localtime())
			cur.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?)", (time_stamp, msg['user']['id'], current_date, current_time, msg['content']['data'],))
			conn.commit()	
			conn.close()			
				
				
		if msg['msg_type_id'] == 4:
			input_pattern = '^("\w+")(,"\w+"){0,49}$'
			if re.match('^\s*today\s*', msg['content']['data']):
			#if msg['content']['data'] == 'today':
				today_date = time.strftime("%Y-%m-%d", time.localtime())
				reply_instruction = query_teacher_instruction(today_date)
			elif re.match('^\s*yesterday\s*', msg['content']['data']):
			#elif msg['content']['data'] == 'yesterday':
				yesterday_date = str(datetime.date.today() - datetime.timedelta(days - 1))
				reply_instruction = query_teacher_instruction(yesterday_date)

#			print msg['user']['name']
#			self.send_msg(msg['user']['name'], msg['content']['data'])
#			self.send_msg_by_uid("群聊消息收到", msg['user']['id'])

##########################################################################################################
		# Code block for forwarding pic(gaowc)
		if msg['content']['type'] == 3:
			received_file = self.get_msg_img(msg['msg_id'])
			

def main():
	bot = myWechatBot()
#	bot.DEBUG = True
	bot.run()
		
if __name__ == '__main__':
	main()