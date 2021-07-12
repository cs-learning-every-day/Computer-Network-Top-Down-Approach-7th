from socket import *
import time

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(3)
start_time = time.time()
end_time = start_time

while True:
    try:
        message, addr = serverSocket.recvfrom(1024)
        messages = message.decode().split()
        rtime = float(messages[1])
        end_time = rtime
        ping = time.time() - rtime
        print(str(messages[0]), ":", ping)
    except Exception as e:
        if start_time == end_time:
            print("Heartbeat continue")
            continue
        if time.time() - end_time >= 1:  # 1秒钟没接收到数据，则判定client停止
            print("Heartbeat pause")
            break
        else:
            print('Packet lost')
serverSocket.close()
