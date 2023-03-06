#!/bin/python
import signal
import os
import sys
import socket
import selectors

# Use this variable for your loop
daemon_quit = False
host = '127.0.0.1'
port = int(sys.argv[1])  # need to change
sel = selectors.DefaultSelector()


# Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1024)
    if data:
        commands(data.decode('UTF-8').replace("\n", ""), conn)
    else:
        sel.unregister(conn)
        conn.close()


def commands(data, sock):
    protocol = data.split(" ")
    protocol[0] = protocol[0]
    if protocol[0] == "REGISTER":
        register_part(protocol, sock)
    elif protocol[0] == "LOGIN":
        login_part(protocol, sock)
    elif protocol[0] == "CREATE":
        create_part(protocol, sock)
    elif protocol[0] == "JOIN":
        join_part(protocol, sock)
    elif protocol[0] == "SAY":
        say_part(protocol, sock)
    elif protocol[0] == "CHANNELS":
        chat_server.channels_command(sock)
    else:
        sock.send("Invalid client request.\n".encode('UTF-8'))


class User:
    def __init__(self, name, password, conn):
        self.name = name
        self.password = password
        self.conn = conn
        self.is_online = False
        self.channels = {}

    def login_process(self, password, conn):
        if password == self.password and conn == self.conn:
            if chat_server.test_online(conn):
                return False
            self.is_online = True
            return True
        return False


class Channel:
    def __init__(self, name, conn):
        self.name = name
        self.conn = conn
        self.contained_users = {}


class ChatServer:
    def __init__(self):
        self.users = {}
        self.channels = {}

    def find_user(self, conn):
        for user in self.users.values():
            if user.conn == conn:
                return user
        return None

    def test_online(self, conn):
        for user in self.users.values():
            if user.conn == conn:
                return user.is_online
        return False

    def register(self, username, password, connection):
        if username in self.users:
            return False
        self.users[username] = User(username, password, connection)
        return True

    def login(self, username, password, conn):
        if username in self.users:
            if self.users[username].is_online:
                return False
            return self.users[username].login_process(password, conn)
        return False

    def join(self, channel_name, conn):
        if not self.test_online(conn) or channel_name not in self.channels:
            return False
        channel_to_join = self.channels[channel_name]
        user = self.find_user(conn)
        if self.find_user(conn) is None or user.name in channel_to_join.contained_users:
            return False
        channel_to_join.contained_users[user.name] = user
        user.channels[channel_name] = channel_to_join
        return True

    def create(self, channel_name, conn):
        if not self.test_online(conn) or channel_name in self.channels:
            return False
        self.channels[channel_name] = Channel(channel_name, conn)
        return True

    def say(self, channel_name, message, conn):
        if not self.test_online(conn) or channel_name not in self.channels:
            return False
        channel_to_say = self.channels[channel_name]
        if self.find_user(conn) is None or self.find_user(conn).name not in channel_to_say.contained_users:
            return False
        for user in channel_to_say.contained_users.values():
            if user.is_online:
                msg = "RECV {} {} {}\n".format(self.find_user(conn).name, channel_name, message)
                user.conn.send(msg.encode('UTF-8'))
        return True

    def channels_command(self, conn):
        if not self.test_online(conn) or self.find_user(conn) is None:
            conn.send("RESULT CHANNELS \n".encode('UTF-8'))
            return
        user = self.find_user(conn)
        output = []
        output_str = ""
        for name in user.channels.keys():
            output.append(name)
        output.sort()
        for o in output:
            output_str += o + ", "
        output_str = output_str.strip(", ")
        conn.send("RESULT CHANNELS {}\n".format(output_str).encode('UTF-8'))


def register_part(protocol, sock):
    username = protocol[1]
    password = protocol[2]
    available_register = chat_server.register(username, password, sock)
    if available_register:
        sock.send("RESULT REGISTER 1\n".encode('UTF-8'))
    else:
        sock.send("RESULT REGISTER 0\n".encode('UTF-8'))


def login_part(protocol, sock):
    username = protocol[1]
    password = protocol[2]
    available_login = chat_server.login(username, password, sock)
    if available_login:
        sock.send("RESULT LOGIN 1\n".encode('UTF-8'))
    else:
        sock.send("RESULT LOGIN 0\n".encode('UTF-8'))


def join_part(protocol, sock):
    channel_name = protocol[1]
    conn = sock
    if chat_server.join(channel_name, conn):
        sock.send("RESULT JOIN {} 1\n".format(channel_name).encode('UTF-8'))
    else:
        sock.send("RESULT JOIN {} 0\n".format(channel_name).encode('UTF-8'))


def create_part(protocol, sock):
    channel_name = protocol[1]
    conn = sock
    if chat_server.create(channel_name, conn):
        sock.send("RESULT CREATE {} 1\n".format(channel_name).encode('UTF-8'))
    else:
        sock.send("RESULT CREATE {} 0\n".format(channel_name).encode('UTF-8'))


def say_part(protocol, sock):
    channel_name = protocol[1]
    message = ""
    for string in protocol[2:]:
        message += string + " "
    message = message.strip()
    conn = sock
    available_say = chat_server.say(channel_name, message, conn)
    if not available_say:
        sock.send("RESULT SAY 0\n".encode('UTF-8'))


socket_used = socket.socket()
socket_used.bind((host, port))
socket_used.listen()
socket_used.setblocking(False)
sel.register(socket_used, selectors.EVENT_READ, accept)
chat_server = ChatServer()


def run():
    # Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within
    # the run() function
    while not daemon_quit:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    run()
