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
	
	def query_teacher_instruction(self, msg, query_date):
		conn = sqlite3.connect(self.wechat_DB)
		cur = conn.cursor()
		teacher_instruction = cur.execute("SELECT TIME, CONTENT FROM chat_history WHERE DATE=?", (query_date,))
		output_list = teacher_instruction.fetchall()
		output_str = ""
		
		if output_list.__len__() != 0:
			for item in output_list:
				output_str = output_str + item[0] + '\n' + item[1] + '\n\n'	
			self.send_msg_by_uid(output_str, msg['user']['id'])
		else:
			output_str = "No data."
			
		conn.close()	
	
	def handle_msg_all(self, msg):
		print "=========================================================================="
		#print msg
		for (k, v) in msg.items():
			print "%s => %s" % (k, v)
			
		# group msg_type_id = 3, contact msg_type_id = 4
		if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
#		if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
			print "******************"
			print msg['content']['user']['id']
			print msg['content']['user']['name']
			name_list = self.get_group_member_name(msg['user']['id'], msg['content']['user']['id'])
			print name_list
			print "******************"
			
			# Connect DB. 
#			wechat_DB = 'D:\SQLite\DB_Files\wechatBotDB.db'
			conn = sqlite3.connect(self.wechat_DB)
			cur = conn.cursor()
			
			# Collect user id. Comment this block out when collect user data is done.
			#cur.execute("INSERT OR IGNORE INTO id_list VALUES (?, ?)", (msg['content']['user']['id'], msg['content']['user']['name'],))
			
			# Insert data into DB
			# time_stamp is the primary key in chat_history
			#if msg['user']['id'] == '@fb7d161360c0c80b0aa8d0f5e2dd2a07':
			time_stamp = time.time()
			current_date = time.strftime("%Y-%m-%d", time.localtime())	
			current_time = time.strftime("%H:%M:%S", time.localtime())
			cur.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?, ?, ?)", (time_stamp, msg['content']['user']['id'], name_list['display_name'], name_list['nickname'], current_date, current_time, msg['content']['data'],))
			conn.commit()	
			conn.close()			
				
				
		if msg['msg_type_id'] == 4:
			if re.match('^\s*today\s*$', msg['content']['data']):
				today_date = time.strftime("%Y-%m-%d", time.localtime())
				reply_instruction = self.query_teacher_instruction(msg, today_date)
			elif re.match('^\s*yesterday\s*$', msg['content']['data']):
				yesterday_date = str(datetime.date.today() - datetime.timedelta(days - 1))
				reply_instruction = self.query_teacher_instruction(msg, yesterday_date)

#			print msg['user']['name']
#			self.send_msg(msg['user']['name'], msg['content']['data'])
#			self.send_msg_by_uid("message received", msg['user']['id'])

##########################################################################################################
		# Code block for forwarding pic(gaowc)
		#if msg['content']['type'] == 3:
		#	received_file = self.get_msg_img(msg['msg_id'])
			

def main():
	bot = myWechatBot()
#	bot.DEBUG = True
	bot.run()
		
if __name__ == '__main__':
	main()
