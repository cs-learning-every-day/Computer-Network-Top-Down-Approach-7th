from socket import *
import sys


if len(sys.argv) < 3:
    print("请输入参数 host port file")
    exit(-1)

# python webClient.py 127.0.0.1 9000 HelloWorld.html
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
fileName = sys.argv[3]

request_header = 'GET /%s HTTP/1.1\n' \
                 'Host: localhost:9000\n' \
                 'Purpose: prefetch\n' \
                 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\n' \
                 'Accept-Encoding: gzip, deflate, br\n' \
                 'Accept-Language: zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,und;q=0.6\n' \
                 'Connection: keep-alive\n' % fileName
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.send(request_header.encode())
for i in range(2):
    mod = clientSocket.recv(1024)
    print(mod.decode())
clientSocket.close()
