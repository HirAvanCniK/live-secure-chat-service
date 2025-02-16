import socket, sys, threading, os, datetime, time as t

def logs(message):
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    open(FILELOG_NAME, "a").write(f"[{time}] {message.strip()}\n")

def handle_client(client_socket):
    # Requires client name
    client_socket.send(b'Insert your name\n')
    client_name = client_socket.recv(1024).decode().strip()

    if len(client_name) > 20 or len(client_name) < 5:
        client_socket.send(b"Error: Incorrect name length!\nExit...\n")
        client_socket.close()
    elif client_name in clients.values():
        client_socket.send(b"Error: Name already used!\nExit...\n")
        client_socket.close()
    else:
        if SERVER_KEY != None:
            # Requires server key
            client_socket.send(b'Insert server authentication key\n')
            client_insert_key = client_socket.recv(1024).decode().strip()
            if client_insert_key != SERVER_KEY:
                client_socket.send(b"Error: Invalid key!\nExit...\n")
                client_socket.close()
                return
        else:
            # Welcome message
            welcome_message = f'Welcome, {client_name}!\n'
            client_socket.send(welcome_message.encode())
            logs(f"User logged in as {client_name}")

            # Add the client to the list
            clients[client_socket] = client_name

            # Variable to store the last time the client sent a message
            last_activity_time = datetime.datetime.now().timestamp()

            # Function to check client inactivity
            def check_inactivity():
                while True:
                    t.sleep(10)  # Check every minute
                    if datetime.datetime.now().timestamp() - last_activity_time > 300:  # 5 minutes
                        logs(f"Client {client_name} has been inactive for 5 minutes. Closing connection.")
                        client_socket.send(b"Closing connection for inactivity...")
                        client_socket.close()
                        clients.pop(client_socket)
                        broadcast_message(f"{client_name} has been disconnected due to inactivity\n", client_socket)
                        break

            # Start the inactivity check thread
            inactivity_thread = threading.Thread(target=check_inactivity)
            inactivity_thread.daemon = True
            inactivity_thread.start()

            while True:
                try:
                    # Receive the message sent by the client
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break

                    # Update the last activity time
                    last_activity_time = datetime.datetime.now().timestamp()

                    # Prints the message with the client name
                    message_with_name = f'({client_name}) {data}'
                    logs(message_with_name)

                    # Send the message to all clients except the sender
                    broadcast_message(message_with_name, client_socket)
                except OSError:
                    try:
                        client_socket.send(b"Closing connection...\n")
                    except OSError:
                        pass
                    client_socket.close()
                    logs(f"Client {client_name} has disconnected")
                    try:
                        clients.pop(client_socket)
                    except KeyError:
                        pass
                    broadcast_message(f"{client_name} has disconnected\n", client_socket)
                    break

def broadcast_message(message, client_to_exclude):
    for client in clients.keys():
        if client != client_to_exclude:
            try:
                client.send(message.encode())
            except Exception as e:
                logs(f"Error sending message to client: {e}")
                client.close()
                try:
                    clients.pop(client)
                except KeyError:
                    pass

def get_params():
    if len(sys.argv) == 3:
        try:
            return int(sys.argv[1]), sys.argv[2]
        except:
            return None
    elif len(sys.argv) == 2:
        return int(sys.argv[1]), None
    else:
        return None

if __name__ == "__main__":
    params = get_params()
    if params is None:
        print(f"Usage: python3 {os.path.basename(__file__)} <int:port> [str:server_key]")
    elif params[1] != None and len(params[1]) < 5:
        print(f"Error: Incorrect SERVER_KEY length!")
    else:
        PORT, SERVER_KEY = params
        time = datetime.datetime.now().strftime("%d.%m.%Y %H.%M.%S")
        FILELOG_NAME = f"livechat_{time}.log"

    # log.warn(f"Server random key: {SERVER_KEY.hex()}")
    # print(f"Server key: {'none' if not SERVER_KEY else SERVER_KEY}")
    open("server.key", "w").write('none' if not SERVER_KEY else SERVER_KEY+"\n")

    # List for all clients that will connect
    clients = {}

    # Server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', PORT))
    server.listen()

    logs(f"Listen on {socket.gethostbyname(socket.gethostname())}:{PORT}")
    while True:
        try:
            # Accept a client connection
            client_sock, client_addr = server.accept()

            logs(f"Connection accepted {client_addr[0]}:{client_addr[1]}")

            # Thread to manage the client
            client_handler = threading.Thread(target=handle_client, args=(client_sock,))
            client_handler.start()
        except KeyboardInterrupt:
            logs("Server shutdown...")
            exit(0)
        except:
            pass
