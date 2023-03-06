import socket
import sys
import time

time.sleep(5)
s = socket.socket()
port = int(sys.argv[1])
s.connect(('127.0.0.1', port))
quit_b = False
f = open(sys.argv[2], "r")
w1 = open("register_login_test.out", "w")
commands = f.readlines()
for command in commands[:5]:
    s.send(command.encode('utf-8'))
    time.sleep(1)
    w1.write(s.recv(1024).decode('utf-8'))
w1.close()
w2 = open("create_channel_test.out", "w")
for command in commands[5:9]:
    s.send(command.encode('utf-8'))
    time.sleep(1)
    w2.write(s.recv(1024).decode('utf-8'))
w2.close()
w3 = open("join_channels_test.out", "w")
for command in commands[9:16]:
    s.send(command.encode('utf-8'))
    time.sleep(1)
    w3.write(s.recv(1024).decode('utf-8'))
w3.close()
w4 = open("say_test.out", "w")
for command in commands[16:]:
    s.send(command.encode('utf-8'))
    time.sleep(1)
    w4.write(s.recv(1024).decode('utf-8'))
w4.close()
time.sleep(5)