# -*- coding: utf-8 -*-
import sys
import re
import time
import sqlite3
import datetime
import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from wxbot import *

class myWechatBot(WXBot):

	wechat_DB = './wechatBotDB.db'
	# base_dir = 'D:\Python\Project\wechat_bot\Wechat_Robot-little-wing-patch-2'
	base_dir = os.getcwd()
	
	def query_teacher_instruction(self, msg, query_date):
		conn = sqlite3.connect(self.wechat_DB)
		cur = conn.cursor()
		teacher_instruction = cur.execute("SELECT TIME, CONTENT FROM chat_history WHERE DATE=?", (query_date,))
		output_list = teacher_instruction.fetchall()
		output_str = ""
		
		if output_list.__len__() != 0:
			for item in output_list:
				output_str = output_str + item[0] + '\n' + item[1] + '\n\n'	
		else:
			output_str = "No data."
			
		self.send_msg_by_uid(output_str, msg['user']['id'])	
		conn.close()	
		
	def send_img_mail(self, img_loc, mail_info):
		with open(mail_info, "r") as file:
			for line in file:
				if re.match('Host:*', line):
					mail_host = line[line.find(':')+1:].strip(' ').strip('\r\n')
				elif re.match('From:*', line):
					mail_sender = line[line.find(':')+1:].strip(' ').strip('\r\n')
				elif re.match('Passwd:*', line):
					mail_passwd = line[line.find(':')+1:].strip(' ').strip('\r\n')
				elif re.match('To:*', line):
					mail_receiver = line[line.find(':')+1:].strip(' ').strip('\r\n')
		'''
		mail_host = "smtp.sina.cn"
		mail_user = "benyu_2017@sina.cn"
		mail_passwd = "XXXXXXXX"	
		sender = 'benyu_2017@sina.cn'
		receiver = 'Ben.Yu@nokia-sbell.com'
		
		msgRoot = MIMEMultipart('related')
		msgRoot['From'] = Header('benyu_2017@sina.cn')
		msgRoot['To'] = Header('Ben.Yu@nokia-sbell.com')
		subject = 'Forwarded image from wechat'
		msgRoot['Subject'] = Header(subject)
		'''
		msgRoot = MIMEMultipart('related')
		msgRoot['From'] = Header(mail_sender)
		msgRoot['To'] = Header(mail_receiver)
		subject = 'Forwarded image from wechat'
		msgRoot['Subject'] = Header(subject)		
		
		msgAlternative = MIMEMultipart('alternative')
		msgRoot.attach(msgAlternative)
		mail_msg = """
		<p>Image from wechat</p>
		<p><img src="cid:image1"></p>
		"""
		msgAlternative.attach(MIMEText(mail_msg, 'html'))
		fp = open(img_loc, 'r')
		print "[INFO] Image is located at %s" % img_loc
		msgImage = MIMEImage(fp.read())
		fp.close()
		
		msgImage.add_header('Content-ID', '<image1>')
		msgRoot.attach(msgImage)
		
		try:
			smtpObj = smtplib.SMTP()
			smtpObj.connect(mail_host, 25)
			smtpObj.login(mail_sender, mail_passwd)
			smtpObj.sendmail(mail_sender, mail_receiver, msgRoot.as_string())
			print "[INFO] Mail is sent."
		except smtplib.SMTPException:
			print "[Error] Mail cannot be sent."
	
	def handle_msg_all(self, msg):
		print "=========================================================================="
		print "[INFO] Display msg details:"
		for (k, v) in msg.items():
			print "	%s => %s" % (k, v)
			
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
		
		# Send selected data according to users' query
		if msg['msg_type_id'] == 4:
			if re.match('^\s*today\s*$', msg['content']['data']):
				today_date = time.strftime("%Y-%m-%d", time.localtime())
				reply_instruction = self.query_teacher_instruction(msg, today_date)
			elif re.match('^\s*yesterday\s*$', msg['content']['data']):
				yesterday_date = str(datetime.date.today() - datetime.timedelta(days - 1))
				reply_instruction = self.query_teacher_instruction(msg, yesterday_date)



		# Forward image to Gaowc
		if msg['content']['type'] == 3:
			received_img = ''
			received_img = self.base_dir + '\\temp\\' + self.get_msg_img(msg['msg_id'])
			mail_info = self.base_dir + '\\mail_info.txt'
			self.send_img_mail(received_img, mail_info)

def main():
	bot = myWechatBot()
#	bot.DEBUG = True
	bot.run()
		
if __name__ == '__main__':
	main()
