#!/usr/bin/python
import time
from pprint import pprint
from zapv2 import ZAPv2
#import TestPscanCases
import datetime
import traceback
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
###########################################################
gmail_user = "provide gamil"
gmail_pwd = "provide password"
###########################################################
############################Send Mail######################
def mail(to, subject, text, attach):
   msg = MIMEMultipart()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text))
   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()
##############################################################
try:
    target = 'https://example.com'
    zap = ZAPv2()
    # Use the line below if ZAP is not listening on 8080
    zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})
    # do stuff
    print 'Accessing target %s' % target
    # try have a unique enough session...
    zap.urlopen(target)
    # Give the sites tree a chance to get updated
    time.sleep(1)
    print 'Spidering target %s' % target
    zap.spider.scan(target)
    # Give the Spider a chance to start
    time.sleep(2)
    while (int(zap.spider.status()) < 100):
        print 'Spider progress %: ' + zap.spider.status()
        time.sleep(2)
    print 'Spider completed'
    # Give the passive scanner a chance to finish
    time.sleep(1)
    print 'Scanning target %s' % target
    # Set Injectable Parameters (The sum of 1,2,4,8,18) mean all parameter to test
    zap.ascan.set_option_target_params_injectable(31)
    zap.ascan.enable_all_scanners()
    zap.ascan.scan(target,recurse="example.com")
    while (int(zap.ascan.status()) < 100):
        print 'Scan progress %: ' + zap.ascan.status()
        time.sleep(5)
    print 'Scan completed'
    # Report the results
    print 'Hosts: ' + ', '.join(zap.core.hosts)
    print 'Alerts: '
    pprint (zap.core.alerts())
    # Send Email Html Report to email
    sscanDate = datetime.date.today()
    repoName = "dailyscanReport: " + str(sscanDate) + ".html"
    #script_dir = os.path.dirname(__file__)
    ScanFPath = "/var/log/DailyScan/" + repoName 
    #print ScanFPath  
    send_html =  open(ScanFPath, "a+", 0)
    send_html.write(zap.core.htmlreport())
    SUBJECT = repoName
    mail("yourname@example.com",
    SUBJECT,
    "dailt scan report.",
    ScanFPath)
except Exception, err:
    print(traceback.format_exc())
   # script_dir = os.path.dirname(__file__)
   # print script_dir + "path"
    print "Exception Occurred.!!"
    mail("yourname@example.com","Scanning Disrupted...",traceback.format_exc(),"err")
