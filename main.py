#!/usr/bin/env python3

import socket

from settings import *
from server import *
from request import *
from response import *

def main():
	try:
		server = Server()
		server.run()
	except KeyboardInterrupt:
		server.close()
		print("Exiting!")
	
main()
