#-*- coding: utf-8 -*-
from itemadapter import ItemAdapter
import smtplib
from email.mime.text import MIMEText
from . import mail

class WebtoonbotPipeline:

    def __init__(self):
        self.mailStr = ""

    def process_item(self, item, spider):
        self.mailStr += "title: " + item['title'] + '\n'
        self.mailStr += "content: " + item['content'] + '\n'
        return item

    def close_spider(self, spider):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()      
        smtp.starttls() 
        smtp.login(mail.senderEmail, mail.senderPassword)
        if self.mailStr == "":
            smtp.quit()
            return
        msg = MIMEText(self.mailStr)
        msg['Subject'] = 'I\'m WebtoonBot!'
        msg['To'] = mail.toEmail
        smtp.sendmail(mail.senderEmail, mail.toEmail, msg.as_string())
        smtp.quit()