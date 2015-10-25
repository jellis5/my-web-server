# These tests assume that the server is already running, and is running
# on HOST:PORT as defined in the settings file.

import socket

from settings import *

class Client:
	def __init__(self):
		pass
		
	def get(self, path):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.connect((HOST, PORT))
		s.sendall(bytes("GET {} HTTP/1.0".format(path), 'utf-8'))
		resp = bytes()
		while True:
			data = s.recv(1024)
			if not data:
				break
			resp += data
		print(resp)
		
	def post(self):
		pass

c = Client()
c.get('/test.py')
