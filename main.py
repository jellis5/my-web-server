#!/usr/bin/env python3

import socket

from settings import *
from request import *
from response import *

def main():
	# initialize server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(QUEUED_CONNS)
	# handle client upon connection
	while True:
		try:
			client_s, client_addr = s.accept()
			req = Request(str(client_s.recv(1024), 'utf-8'))
			if req.req_method == 'GET':
				resp = GETResponse(req)
			elif req.req_method == 'POST':
				resp = POSTResponse(req)
			elif req.req_method == 'HEAD':
				resp = HEADResponse(req)
			client_s.sendall(str(resp).encode('utf-8'))
			client_s.close()
		except KeyboardInterrupt:
			client_s.close()
			s.close()
			print("Exiting!")
	
main()
