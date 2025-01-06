from socket import *
import json
import re

def parseRequest(requests: str) -> str | None:
    if len(requests) < 1:
        return None
    
    arRequests = requests.split('\n')
    for line in arRequests:
        match = re.search(r'\b(GET|POST|DELETE|PUT|PATCH)\b\s+(.*?)\s+HTTP/1.1', line)
        if match:
            strMethod = match.group(1)
            print(strMethod)
            strPath = match.group(2)
            return strPath
    return None

def getUserList():
    return [
        {'id': 1, 'name': 'Trump'},
        {'id': 2, 'name': 'Biden'},
        {'id': 3, 'name': 'Obama'},
    ]

def createServer():
    arPath = ['/', '/user/list', '/google.png']
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080))
        serverSocket.listen()
        while True:
            (connectionSocket, addr) = serverSocket.accept() # Blocking
            print('Connection received from ', addr)
            
            request = connectionSocket.recv(4096).decode('utf-8')
            print(request)
            strPath = parseRequest(request)
            print(f'Path: {strPath}')
            if strPath is None:
                connectionSocket.shutdown(SHUT_WR)
                continue
            
            if strPath is None:
                print(connectionSocket)
                connectionSocket.shutdown(SHUT_WR)
                print('socket will shutdown')
                continue
            
            if strPath not in arPath:
                print('Resource not found')
                response = 'HTTP/1.1 404 Not Found\n'
                response += 'Content-Type: text/html\n'
                response += '\n'
                response += '<html><body>404 Not Found</body></html>\n'
                connectionSocket.sendall(response.encode('utf-8'))
                connectionSocket.shutdown(SHUT_WR)
                continue
            
            response = 'HTTP/1.1 200 OK\n'
            if strPath == '/user/list':
                response += 'Content-Type: application/json\n'
                response += '\n'
                response += json.dumps(getUserList())
            elif strPath == '/':
                response += 'Content-Type: text/html\n'
                response += '\n'
                response += '<html><body>Hello World<br /><img src="/google.png" /></body></html>\n'
            elif strPath == '/google.png':
                response += 'Content-Type: image/png\n'
                response += '\n'
                connectionSocket.sendall(response.encode('utf-8'))
                with open('google.png', 'rb') as f:
                    while chunk := f.read(1024):
                        connectionSocket.sendall(chunk)
                connectionSocket.shutdown(SHUT_WR)
                continue

            connectionSocket.sendall(response.encode('utf-8'))
            connectionSocket.shutdown(SHUT_WR)
            
    except KeyboardInterrupt:
        print('\nShutting down the server\n')
        serverSocket.close()
    except Exception as e:
        print('Unexpected error:', e)
        
if __name__ == '__main__':
    createServer()