import socket, threading

from settings import *
from client import *

class Server:
	def __init__(self):
		self.host = HOST
		self.port = PORT
		self.max_listen_queue = QUEUED_CONNS
		self.listen_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listen_s.bind((HOST, PORT))
		self.listen_s.listen(QUEUED_CONNS)
		self.threads = []
		
	def run(self):
		while True:
			client = Client(*self.listen_s.accept())
			client.start()
			self.threads.append(client)
			
	def close(self):
		for t in self.threads:
			t.join()
		self.listen_s.close()
