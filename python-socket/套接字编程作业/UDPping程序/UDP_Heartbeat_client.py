from socket import *
import time

serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
for i in range(1, 11):
    if i == 9:  # 模拟数据包丢失
        clientSocket.sendto("".encode(), (serverName, serverPort))
        continue
    t = time.time()
    time.sleep(0.5)
    message = str(i) + " " + str(t)
    clientSocket.sendto(message.encode(), (serverName, serverPort))

clientSocket.close()
