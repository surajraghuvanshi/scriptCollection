import paramiko
import sys
import time

#A function that logins and execute commands
def sshtest(host):
  HOST = host
  sshclient=paramiko.SSHClient()
  #Add missing client key
  sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  sshclient.connect(HOST,username="local",password="local",compress = True,look_for_keys=False, allow_agent=False)
  print "SSH connection to %s established" %HOST
  sshclient.close()
  print "Logged out of device %s" %HOST

#for loop to call above fn x times. Here x is set to 3
domainlist = [line.rstrip() for line in open('1.txt', 'r')]
for i in domainlist:
    print i.strip()
    sshtest(i.strip())
