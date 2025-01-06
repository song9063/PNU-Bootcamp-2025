from socket import *

def createServer():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080))
        serverSocket.listen()
        while True:
            (connectionSocket, addr) = serverSocket.accept() # Blocking
            print('Connection received from ', addr)
            
            request = connectionSocket.recv(1024).decode('utf-8')
            print(request)
            
            response = 'HTTP/1.1 200 OK\n'
            response += 'Content-Type: text/html\n'
            response += '\n'
            response += '<html><body>Hello World</body></html>\n'
            connectionSocket.sendall(response.encode('utf-8'))
            connectionSocket.shutdown(SHUT_WR)
            
    except KeyboardInterrupt:
        print('\nShutting down the server\n')
        serverSocket.close()
        
if __name__ == '__main__':
    createServer()