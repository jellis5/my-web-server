import re

from settings import *

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
