import socket
import sys
import signal
import time

# Creating a class of signals to process some errors
class Stopper:
    stop = False
    def __init__(self):
        signal.signal(signal.SIGQUIT, self.interrupt_handler)
        signal.signal(signal.SIGTERM, self.interrupt_handler)
        signal.signal(signal.SIGINT, self.interrupt_handler)

    def interrupt_handler(self, *args):
        self.stop = True


BUFFER_SIZE = 10000
port = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", port))
sock.settimeout(10)
sock.listen(1)


def proc(clientSock):
    clientSock.send(b"accio\r\n")

    try:
        total = 0
        while True:
            m = clientSock.recv(1)

            if not m:
                break

            total += len(m)

        print(total)
        clientSock.close()

    except socket.error:
        sys.stderr.write("ERROR: ()Address-related error connecting to server")
        exit(1)



stopping = Stopper()

while not stopping.stop:
    clientSock, addr = sock.accept()
    proc(clientSock)


sock.close
