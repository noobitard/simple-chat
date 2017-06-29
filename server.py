import socket, select

def broadcastMessage(sock, message):
    for socket in connectionList:
        if socket != serverSocket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                connectionList.remove(socket)

if __name__ == '__main__':

    connectionList = []
    recvBuff = 4096
    port = 5000

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('127.0.0.1', port))
    serverSocket.listen(20)

    connectionList.append(serverSocket)

    print "Chat server started on port " + str(port)

    while 1:
        readSockets, writeSockets, errorSockets = select.select(connectionList, [], [])
        for sock in readSockets:
            if sock == serverSocket:
                sockfd, addr = serverSocket.accept()
                connectionList.append(sockfd)
                print "Client (%s, %s) connected\n" % addr

                broadcastMessage(sockfd, "(%s:%s) entered room \n"%addr)
            else:
                try:
                    data = sock.recv(recvBuff)
                    if data:
                        broadcastMessage(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                except:
                    broadcastMessage(sock, "Client (%s, %s) is offline\n" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    connectionList.remove(sock)
                    continue
    serverSocket.close()
            
