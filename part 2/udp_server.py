
import socket
import time
def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # socket to listen on port 8855 ('') listen on all available network
    server_socket.bind(('', 8855))
    clients = {}
    count = 0

    while True:
        data, address = server_socket.recvfrom(1024)
        client_name = data.decode()
        # to count number of client sent messages
        count += 1 if address not in clients else 0
        timestamp = time.time()
        local_time = time.localtime(timestamp)
        formatted_time = time.strftime("%H:%M:%S", local_time)
        dict = {"client_name": client_name, "time": formatted_time}
        clients[address] = dict
        
        # Note to self: add[0] ip add, add[1] is represents the port number
        print(
            f"Received message from {client_name} at {formatted_time}  , at: {address[0]}:{address[1]}")

        if count >= 3:
            print("Server First Name Last Name:")
            for idx, (addr, name) in enumerate(clients.items(), start=1):
                print(
                    f"{idx}- received message from {name} at {addr[0]}:{addr[1]}")

            count = 0
            clients = {}


print("[SERVER] is running...")
udp_server()
