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

sock.bind(("0.0.0.0", int(port)))
sock.settimeout(10)
sock.listen(5)


def proc(clientSock, addr):
    clientSock.send(b"accio\r\n")

    total = 0
    while True:
        m = clientSock.recv(1)

        if not m:
            break

        total += len(m)

    print(total)
    clientSock.close()


stopping = Stopper()

while not stopping.stop:
    try:
        clientSock, addr = sock.accept()
        proc(clientSock, addr)

    except socket.timeout:
        continue

    except Exception:
        continue

sock.close
