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
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080))
        serverSocket.listen()
        while True:
            (connectionSocket, addr) = serverSocket.accept() # Blocking
            print('Connection received from ', addr)
            
            request = connectionSocket.recv(1024).decode('utf-8')
            print(request)
            strPath = parseRequest(request)
            print(f'Path: {strPath}')
            
            response = 'HTTP/1.1 200 OK\n'
            if strPath == '/user/list':
                response += 'Content-Type: application/json\n'
                response += '\n'
                response += json.dumps(getUserList())
            else:
                response += 'Content-Type: text/html\n'
                response += '\n'
                response += '<html><body>Hello World</body></html>\n'
            connectionSocket.sendall(response.encode('utf-8'))
            connectionSocket.shutdown(SHUT_WR)
            
    except KeyboardInterrupt:
        print('\nShutting down the server\n')
        serverSocket.close()
    except Exception as e:
        print('Unexpected error:', e)
        
if __name__ == '__main__':
    createServer()