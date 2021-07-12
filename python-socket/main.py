import socket
url = 'www.baidu.com'
port = 80
# 创建TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接服务端
sock.connect((url, port))
# 创建请求消息头
request_url = 'GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n'
# 发送请求
# sock.send(request_url.encode())
response = b''
# 接收返回的数据

fp = sock.makefile('rb', 0)
sock.send(request_url.encode())
print(fp.read())
fp.close()
