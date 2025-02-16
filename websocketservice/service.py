import asyncio, sys, websockets, socket, threading

class TCP():
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def write(self, data: bytes) -> bool:
        try:
            self.server.send(data)
            return True
        except:
            return False

    def read(self) -> bytes:
        try:
            return self.server.recv(1024)
        except:
            return b''

def put_messages(server: TCP, ws, loop):
    while True:
        data = server.read()
        if data:
            asyncio.run_coroutine_threadsafe(ws.send(data.decode()), loop)

async def handler(websocket):
    tcp_server = TCP(TCP_HOST, TCP_PORT)
    loop = asyncio.get_event_loop()
    threading.Thread(target=put_messages, args=(tcp_server, websocket, loop), daemon=True).start()
    
    async for message in websocket:
        if tcp_server.write(message.encode()+b"\n"):
            await websocket.send(message)
        else:
            await websocket.send("Error sending message")

async def start_server():
    async with websockets.serve(handler, WS_HOST, WS_PORT):
        print(f"Listen on {socket.gethostbyname(socket.gethostname())}:{WS_PORT}")
        await asyncio.Future()

def get_params():
    if len(sys.argv) != 4:
        return None
    return sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

if __name__ == '__main__':
    params = get_params()
    if params is None:
        exit(1)
    TCP_HOST = params[0]
    TCP_PORT = params[1]

    WS_HOST = '0.0.0.0'
    WS_PORT = params[2]
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        exit(0)
    except:
        exit(1)
