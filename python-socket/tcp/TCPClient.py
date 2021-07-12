from socket import *

serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    try:
        sentence = input('Input lowercase sentence:')
        clientSocket.send(sentence.encode())
        modifiedSentence, serverAddress = clientSocket.recvfrom(1024)
        print("From {0}: {1}".format(serverAddress, modifiedSentence.decode()))
    except KeyboardInterrupt:
        break
    except EOFError:
        break
clientSocket.close()
print("Client Close")
