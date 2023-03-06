import socket
import sys
import time

s = socket.socket()
port = int(sys.argv[1])
s.connect(('127.0.0.1', port))
quit_b = False
f = open(sys.argv[2], "r")
commands = f.readlines()
for command in commands:
    s.send(command.encode('utf-8'))
    time.sleep(1)
    print(s.recv(1024).decode('utf-8'))