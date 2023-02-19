import socket
import sys
import signal
import time

# Creating a class of signals to process some errors
class Stopper:
    stop = False
    def _init_(self):
        signal.signal(signal.SIGQUIT, self.interrupt_handler)
        signal.signal(signal.SIGTERM, self.interrupt_handler)
        signal.signal(signal.SIGINT, self.interrupt_handler)

    def interrupt_handler(self, *args):
        self.stop = True

#
BUFFER_SIZE = 10000

#Getting all of the inputs from the command line
#If port is too large or too mall error?????????/
#Honetly just checks if argv length is at least 2
try:
    port = sys.argv[1]
except Exception:
    sys.stderr.write("Error: () Wrong port number")



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("0.0.0.0", int(port)))

sock.listen(1)

msg = b""
total = 0
stopping = Stopper()
while not stopping.stop: #infinite loop that keeps it connected to client

    clientSock, addr = sock.accept()
    clientSock.settimeout(10) #addr

    clientSock.send(b"accio\r\n")

    while True:
        m = clientSock.recv(1)
        msg += m

        total += len(m)

        if m.find(b"\n") != -1:
            break

        # Connection is closed by server
        elif len(m) <= 0:
            break

    print("Total bits recorded: %d" % total)

    clientSock.close()
