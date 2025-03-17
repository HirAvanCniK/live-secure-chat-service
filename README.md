# Live Secure Chat Service

![Live Secure Chat Service Network](https://raw.githubusercontent.com/HirAvanCniK/live-secure-chat-service/refs/heads/main/webservice/static/imgs/favicon.ico)

The **Live Secure Chat Service** is a real-time chat service that ensures privacy and security through the use of the Tor network. This service offers two connection modes: one via a web interface and another via a TCP connection, both protected by the encryption and anonymity provided by Tor.

## How It Works

The service consists of two main components:

1. **Web Service**: A web interface accessible via a browser, allowing users to chat securely and anonymously.
2. **TCP Service**: A chat service via TCP connection, ideal for applications requiring direct and secure communication between client and server.

Both services are configured to operate exclusively through the Tor network, ensuring user anonymity and communication security.

## Installation

To install and configure the Live Secure Chat Service, follow these steps:

```bash
git clone https://github.com/HirAvanCniK/live-secure-chat-service.git
cd live-secure-chat-service
```

## Setup

### 1. Setting up environment variables

Edit the `start.sh` file by changing the values of the environment variables: `(WEBSOCKET_PORT|TCP_PORT|WEB_PORT|SERVER_KEY)`.

**The `SERVER_KEY` variable can also be empty, but in this case everyone can access the service and chat.**

### 2. Configure the hidden service

If you already have the `torcc` file, simply edit the existing one with the settings in the `torcc` file in this repo.

These are the default paths to the Tor services file in each Operating System

- ***Linux***: `/etc/tor/torrc`
- ***Windows***: `C:\Users\<your-username>\Desktop\Tor Browser\Browser\TorBrowser\Data\Tor\torrc`
- ***macOS***: `/usr/local/etc/tor/torrc`

**IMPORTANT: You must change the path to the `hidden_service` folder written in `torcc` as you wish so that it is accessible and has the necessary permissions to access it.**

### 3. Start the Service

Now you just need to run the `start.sh` file.

```bash
./start.sh
```

### 4. Enjoy your secure service :)

You can find the onion hostname of your service in the `hidden_service` folder named `hostname`.

Hint: To access it via tcp perhaps you would need this
```bash
sudo apt install torsocks
torsocks nc <hostname> <port>
```

Of course, this live chat service can also be used without being under tor network but doing so is no longer secure.
