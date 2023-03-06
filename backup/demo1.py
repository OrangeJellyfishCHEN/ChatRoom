import signal
import socket
import selectors

sel = selectors.DefaultSelector
def read(skt, mask):
    try:
        data = skt.recv(1024)
        if data:
            print("*")
        else:
            sel.unregister()
            skt.close()
    except:
        sel.unregister()


def accept(sock, mask):
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


sock = socket.socket()
sock.bind(('127.0.0.1', 8080))
sock.listen()
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

daemon_quit = False

def quit_gracefully(signum, frame):
    global daemon_quit
    print("quit")
    daemon_quit = True

def run():
    signal.signal(signal.SIGINT, quit_gracefully())
    while not daemon_quit:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
        print("already quit")