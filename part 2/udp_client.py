
import socket
import time
port = 8855
serverName = '192.168.230.255'


def udp(name):
    # AF_INET tells socket to use IPv4 addressing and SOCK_DGRAm it to tell it to use
    clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # enable broadcasting on the socket
    clisocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # allows reusing the address of a previously bound socket
    clisocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c = 0
    print(f"Client Name: {name}")
    while c < 100:
        print(f"Sending message number {c}")
        # Note to self using <brodcast> allows os to determine the appropriate bordcast ip
        # Dr req said to calculate it manually so i put it based on my network configarations
        clisocket.sendto(name.encode(), (serverName, port))  # <'brodcast'>
        time.sleep(2)
        c += 1


name = "Lotfi Qasim"
udp(name)
