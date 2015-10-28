import socket, queue, concurrent.futures

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
		self.thread_queue = queue.Queue()
		self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
		
	def serve(self):
		client_s, client_ip = self.thread_queue.get()
		req = Request(str(client_s.recv(1024), 'utf-8'))
		if req.req_method == 'GET':
			resp = GETResponse(req)
		elif req.req_method == 'POST':
			resp = POSTResponse(req)
		elif req.req_method == 'HEAD':
			resp = HEADResponse(req)
		client_s.sendall(bytes(str(resp), 'utf-8'))
		client_s.close()
		
	def run(self):
		with self.thread_pool as executor:
			while True:
				self.thread_queue.put(self.listen_s.accept())
				while not self.thread_queue.empty():
					executor.submit(self.serve)
			
	def close(self):
		self.listen_s.close()
