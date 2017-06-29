import socket, select, string, sys, threading, os
 
def prompt() :
    sys.stdout.write('<You>: ')
    sys.stdout.flush()

def recvMessage(sock):
    while 1:
        readSocks, writeSocks, errSocks = select.select([sock], [], [])
        try:
            data = readSocks[0].recv(1024)
            if data:
                sys.stdout.write(data)
                prompt()
        except:
            print '\nDisconnected from chat server'
            os._exit(1)
        
def sendMessage(sock):
    while 1:
        msg = sys.stdin.readline()
        try:
            s.send(msg)
            prompt()
        except:
            print "\nDisconnected from chat server"
            os._exit(1)

if __name__ == "__main__":
     
    host = '127.0.0.1'
    port = 5000
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        os._exit(1)
     
    print 'Connected to remote host. Start sending messages'
    prompt()
    threading.Thread(target=recvMessage, args=(s,)).start()
    threading.Thread(target=sendMessage, args=(s,)).start()
