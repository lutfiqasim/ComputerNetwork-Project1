
import socket
import time
port = 8855
serverName = '192.168.1.255'


def udp(name):
    # AF_INET tells socket to use IPv4 addressing and SOCK_DGRAm it to tell it to use
    clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clisocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    clisocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c = 0
    while c < 100:
        # Note to self using <brodcast> allows os to determine the appropriate bordcast ip
        # Dr req said to calculate it manually so i put it based on my network configarations
        clisocket.sendto(name.encode(), (serverName, port))  # <'brodcast'>
        time.sleep(1)
        c += 1


name = "Nsrallah Dweib"
udp(name)
