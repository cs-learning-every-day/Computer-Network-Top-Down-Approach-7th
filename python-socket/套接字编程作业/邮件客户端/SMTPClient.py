from socket import *
import base64

# [SMTP WIKI](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol#SMTP_transport_example)
# [使用telnet 登录163 邮箱](https://www.jianshu.com/p/55c634454362)


# Mail content
subject = "专升本新闻速递！！！"
contentType = "text/plain"
msg = "I love computer networks!"
endmsg = "\r\n.\r\n"

fromAddress = "xmcxhcoder@163.com"
toAddress = "1394466835@qq.com"

# 163 mail config
username = "xmcxhcoder@163.com"
password = "JRILLCXVRBKLSLDF"

# Auth information (Encode with base64)
username = base64.b64encode(username.encode()).decode()
password = base64.b64encode(password.encode()).decode()

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.163.com"
# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# 开始认证登录 base64加密
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

clientSocket.sendall(('%s\r\n' % username).encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

clientSocket.sendall(('%s\r\n' % password).encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command and print server response.
clientSocket.send(('MAIL FROM:<%s>\r\n' % fromAddress).encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
clientSocket.send(('RCPT TO:<%s>\r\n' % toAddress).encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

addresses = [
    {'name': '倪', "email": "1132242721@qq.com"},  # 某倪
    {'name': '李', "email": "1176355274@qq.com"},  # 某李
    {'name': '杜', "email": '3481831237@qq.com'},  # 某杜
    {'name': '丁', "email": '2155508762@qq.com'},  # 某丁
    {'name': '邵', "email": '1921719677@qq.com'},  # 某邵
    {'name': '刘', "email": '1551294119@qq.com'},
    {'name': '杨', "email": '1078512296@qq.com'},
    {'name': '杨', "email": '415340395@qq.com'},
    {'name': '王', "email": '1067198827@qq.com'},
]

moreToSegment = ''
for i in addresses:
    clientSocket.send(('RCPT TO:<%s>\r\n' % i["email"]).encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server.')
    else:
        moreToSegment += 'To:%s <%s>\r\n' % (i["name"], i["email"])

# Send DATA command and print server response.
clientSocket.send('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
# 普通文本信息
# message = ('From:{} <{}>\r\n' \
#            'To:{} <{}>\r\n' \
#            '{}' \
#            'Subject:{}\r\n' \
#            'Content-Type:{}\r\n' \
#            '\r\n {}{}') \
#     .format("XmchxCoder(做个好人)", fromAddress,
#             '孙某', toAddress,
#             moreToSegment,
#             subject, contentType,
#             msg, endmsg)

# html
img = 'https://seopic.699pic.com/photo/50109/8739.jpg_wh1200.jpg'
msg = '<html><body><h2>3天你可能提升不了100分，但是你可能可以冲6次。</h2> <img src="%s"></body></html>' % img
print(msg)
contentType = "text/html"
message = ('From:{} <{}>\r\n' \
           'To:{} <{}>\r\n' \
           '{}' \
           'Subject:{}\r\n' \
           'Content-Type:{}\r\n' \
           '\r\n {}{}') \
    .format("XmchxCoder(做个好人)", fromAddress,
            '孙某', toAddress,
            moreToSegment,
            subject, contentType,
            msg, endmsg)

# local img
# with open("../../resourse/girl-friend.jpg", 'rb') as reader:
#     img = base64.b64encode(reader.read()).decode()
# contentType = "image/JPEG"
# message = ('From:{} <{}>\r\n' \
#            'To:{} <{}>\r\n' \
#            'Subject:{}\r\n' \
#            'Content-Type:{}\r\n' \
#            'Content-transfer-encoding:base64\r\n' \
#            '\r\n {}{}') \
#     .format("XmchxCoder(做个好人)", fromAddress,
#             '孙某', toAddress,
#             subject, contentType,
#             img, endmsg)

clientSocket.send(message.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')
# Message ends with a single period.
clientSocket.sendall('QUIT\r\n'.encode())
# Send QUIT command and get server response.
clientSocket.close()
