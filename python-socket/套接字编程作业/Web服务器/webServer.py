# import socket module
import logging
import threading
from socket import *
import colorlog
from concurrent.futures import ThreadPoolExecutor


# 处理每个Http请求
def thread_function(connection_socket, _addr):
    name = threading.current_thread().getName()
    logger.info("Thread %s: starting", name)

    try:
        message = connection_socket.recv(1024).decode()
        filename = message.split()[1]
        if filename == '/':
            raise IOError
        f = open(filename[1:])
        outputdata = f.read()
        # Send one HTTP header line into socket
        header = 'HTTP/1.1 200 OK\n' \
                 'Connection: close\n' \
                 'Content-Type: text/html\n' \
                 'Content-Length: %d\n\n' % (len(outputdata))
        connection_socket.send(header.encode())

        # Send the content of the requested file to the client
        connection_socket.send(outputdata.encode())
        logger.info("Thread %s: finishing", name)
        connection_socket.close()
    except IOError:
        # Send response message for file not found
        header = 'HTTP/1.1 404 Not Found'
        connection_socket.send(header.encode())
        # Close client socket
        connection_socket.close()


def init_logger(dunder_name, testing_mode) -> logging.Logger:
    log_format = (
        '%(asctime)s - '
        '%(message)s'
    )
    bold_seq = '\033[1m'
    colorlog_format = (
        f'{bold_seq} '
        '%(log_color)s '
        f'{log_format}'
    )
    colorlog.basicConfig(format=colorlog_format)
    logger = logging.getLogger(dunder_name)

    if testing_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger


if __name__ == '__main__':
    logger = init_logger(__name__, testing_mode=False)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    serverPort = 9000
    serverSocket.bind(('', serverPort))
    serverSocket.listen(3)

    pool = ThreadPoolExecutor(3)

    while True:
        # Establish the connection
        try:
            logger.info("Ready to serve...")
            connectionSocket, addr = serverSocket.accept()

            pool.submit(thread_function, connectionSocket, addr)
        except:
            logger.warning("Exit")
            break
    serverSocket.close()
