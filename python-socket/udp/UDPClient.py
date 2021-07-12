from socket import *

serverName = 'localhost'
serverPort = 12000

# IPv4  UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    try:
        message = input('Input lowercase sentence:')
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print("from {} recv: {}".format(serverAddress, modifiedMessage.decode()))
    except KeyboardInterrupt:
        break
    except EOFError:
        break
print("Client Close")
clientSocket.close()
