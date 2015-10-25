import threading

from request import *
from response import *

class Client(threading.Thread):
	def __init__(self, client_s, client_addr):
		super().__init__()
		self.s = client_s
		self.ip, self.port = client_addr
		
	def run(self):
		req = Request(str(self.s.recv(1024), 'utf-8'))
		if req.req_method == 'GET':
			resp = GETResponse(req)
		elif req.req_method == 'POST':
			resp = POSTResponse(req)
		elif req.req_method == 'HEAD':
			resp = HEADResponse(req)
		self.s.sendall(bytes(str(resp), 'utf-8'))
		self.s.close()
		
