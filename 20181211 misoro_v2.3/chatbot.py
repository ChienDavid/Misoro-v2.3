#!/usr/bin/env python
# license removed for brevity
#******************************************************************
#***************************** david ******************************
#******************************************************************
# Author       : Chien Van Dang
# Updated date : 12th July 2018
#
# Application  : ChatScript interaction
#
#******************************************************************
#******************************************************************
#==================================================================
from optparse import OptionParser
import socket
import sys

#==================================================================
class chatbot:

	def __init__(self, user_name, agent_name):
	    self.agentName = agent_name
	    self.userName = user_name

	def toChatScript(self, request):
	    server = "127.0.0.1"
	    port = 1024

	    # Ensure empty strings are padded with atleast one space before sending to the server, as per the required protocol
	    s = request
	    if s == "":
		s = " "

	    # Send this to the server: Put in null terminations as required
	    msg = u'%s\u0000%s\u0000%s\u0000' % (self.userName, self.agentName, s)

	    # Return the response
	    resp = self.sendAndReceiveChatScript(msg, server=server, port=port)
	    if resp is None:
		resp = "Error communicating with Chat Server"
	    return resp

	def sendAndReceiveChatScript(self, msgToSend, server='127.0.0.1', port=1024, timeout=10):
	    try:
		# Connect, send, receive and close socket. Connections are not persistent
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(timeout)  # timeout in secs
		s.connect((server, port))
		#print ('server started and listening')
		s.sendall(msgToSend)
		#print ('sent the message')
		msg = ''
		while True:
		    chunk = s.recv(1024)
		    if chunk == b'':
		        break
		    msg = msg + chunk.decode("utf-8")
		    #print msg
		s.close()
		return msg
	    except:
		return None


