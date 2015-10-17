import subprocess, os, sys

from settings import *

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
		self.httpver = 1.0
		
	def add_header(self, name, value):
		self.resp_header_lines.append("{}: {}".format(name, value))
		
	def create_resp(self):
		raise NotImplementedError("Must be implemented in subclass!")
	
	def __str__(self):
		resp = "\r\n".join(self.resp_header_lines) + "\r\n\r\n"
		if self.resp_body:
			resp += self.resp_body
		return resp
		
class HEADResponse(Response):
	def __init__(self, req):
		super().__init__(req)
		self.create_resp()
		
	def create_resp(self):
		req_path = WEB_ROOT + Response.get_file_from_path(self.req.req_path)
		if os.path.isfile(req_path):
			self.status_code = 200
		else:
			self.status_code = 404
		self.status_msg = Response.status_msg[self.status_code]
		self.resp_header_lines.append(Response.first_line.format(httpver=self.httpver, status_code=self.status_code, status_msg=self.status_msg))
		self.add_header('Content-Type', 'text/html')
		
class GETResponse(Response):
	def __init__(self, req):
		super().__init__(req)
		self.create_resp()
		
	def create_resp(self):
		req_path = WEB_ROOT + Response.get_file_from_path(self.req.req_path)
		if os.path.isfile(req_path):
			self.status_code = 200
			if req_path.endswith('.py'):
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
		req_path = WEB_ROOT + Response.get_file_from_path(self.req.req_path)
		if os.path.isfile(req_path):
			self.status_code = 200
			if req_path.endswith('.py'):
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
