import socket, sys, re, os, subprocess

HOST = 'localhost'
PORT = 8000
QUEDED_CONNS = 1
WEB_ROOT = "/home/jacob/www"

HTTP_METHODS = ('GET', 'POST')

class Request:
	method_line_pattern = re.compile(r'({methods}) (/.*) (HTTP/1\.[01])'.format(methods='|'.join(HTTP_METHODS)), re.IGNORECASE)
	
	def __init__(self, req):
		self.req = req
		self.req_lines = self.req.split("\r\n")
		self.req_method = None
		self.req_path = None
		self.req_httpver = None
		self.parse_req()
		
	def parse_req(self):
		self.req_method, self.req_path, self.req_httpver = Request.method_line_pattern.match(self.req_lines[0]).groups()
		if self.req_method == 'GET':
			try:
				self.query_string = self.req_path.split("?")[1]
			except IndexError:
				self.query_string = None
		elif self.req_method == 'POST':
			self.post_body = self.req_lines[-1]
		
	def __str__(self):
		return self.req
		
class Response:
	# map codes to msgs
	status_msg = {200: 'OK',\
					404: 'Not Found'}
	first_line = "HTTP/{httpver} {status_code} {status_msg}"
	
	@staticmethod
	def get_file_from_path(url_path):
		try:
			return url_path.split("?")[0]
		except IndexError:
			return url_path
	
	def __init__(self, req):
		self.req = req
		self.resp_header_lines = []
		self.resp_body = ""
		self.status_code = None
		self.status_msg = None
		
	def add_header(self, name, value):
		self.resp_header_lines.append("{}: {}".format(name, value))
		
	def create_resp(self):
		raise NotImplementedError("Must be implemented in subclass!")
	
	def __str__(self):
		resp = "\r\n".join(self.resp_header_lines) + "\r\n\r\n"
		if self.resp_body:
			resp += self.resp_body
		return resp
		
class GETResponse(Response):
	def __init__(self, req):
		super().__init__(req)
		self.create_resp()
		
	def create_resp(self):
		self.httpver = 1.0
		
		req_path = WEB_ROOT + Response.get_file_from_path(self.req.req_path)
		if os.path.isfile(req_path):
			self.status_code = 200
			if req_path[-3:] == '.py':
				self.resp_body += str(subprocess.check_output(["python3.4", req_path, str(self.req.query_string)]), 'utf-8')
			else:
				with open(req_path) as f:
					while True:
						fData = f.read(1024)
						if fData:
							self.resp_body += fData
						else:
							break
		else:
			self.status_code = 404
		self.status_msg = Response.status_msg[self.status_code]
		self.resp_header_lines.append(Response.first_line.format(httpver=self.httpver, status_code=self.status_code, status_msg=self.status_msg))
		self.add_header('Content-Type', 'text/html')
		
class POSTResponse(Response):
	def __init__(self, req):
		super().__init__(req)
		self.create_resp()
		
	def create_resp(self):
		self.httpver = 1.0
		
		req_path = WEB_ROOT + Response.get_file_from_path(self.req.req_path)
		if os.path.isfile(req_path):
			self.status_code = 200
			if req_path[-3:] == '.py':
				self.resp_body += str(subprocess.check_output(["python3.4", req_path, str(self.req.post_body)]), 'utf-8')
			else:
				with open(req_path) as f:
					while True:
						fData = f.read(1024)
						if fData:
							self.resp_body += fData
						else:
							break
		else:
			self.status_code = 404
		self.status_msg = Response.status_msg[self.status_code]
		self.resp_header_lines.append(Response.first_line.format(httpver=self.httpver, status_code=self.status_code, status_msg=self.status_msg))
		self.add_header('Content-Type', 'text/html')

def main():
	# initialize server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(QUEDED_CONNS)
	# handle client upon connection
	while True:
		try:
			client_s, client_addr = s.accept()
			req = Request(str(client_s.recv(1024), 'utf-8'))
			if req.req_method == 'GET':
				resp = GETResponse(req)
			elif req.req_method == 'POST':
				resp = POSTResponse(req)
			client_s.sendall(str(resp).encode('utf-8'))
			client_s.close()
			#s.close()
		except KeyboardInterrupt:
			client_s.close()
			s.close()
			print("Exiting!")
	
main()
