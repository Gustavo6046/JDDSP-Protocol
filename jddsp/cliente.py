import socket
import sys
import time
from threading import Thread

if __name__ != "__main__":
    exit()


def get_output(client):
    while True:
        data = ""

        while True:
            try:
                data += client.recv(4096)

            except socket.error:
                time.sleep(0.2)
                continue

            if not data.endswith("\n"):
                time.sleep(0.2)
                continue

            break

        lines = [line.rstrip("\r") for line in data.split("\n") if line.rstrip("\r") != ""]

        for line in lines:
            print line


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((sys.argv[1], int(sys.argv[2])))

except IndexError:
    print "Provide a IP and a port argument!"
    exit()

Thread(target=get_output, args=(sock,)).start()

while True:
    sock.sendall(raw_input())
    time.sleep(0.11)
    print ">",
