import socket
import sys
import time
s = socket.socket()
s.connect(('127.0.0.1', 8080))
s.send("^C".encode("utf-8"))
s.send("^C".encode("utf-8"))
