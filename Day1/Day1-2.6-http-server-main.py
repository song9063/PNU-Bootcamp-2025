from socket import *
import json
import re
from enum import Enum
from dataclasses import dataclass

class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'

class HTTPStatusCode(Enum):
    OK = (200, 'OK')
    NOT_FOUND = (404, 'Not Found')
    SEE_OTHER = (303, 'See Other')
    SERVER_ERROR = (500, 'Internal Server Error')

class HttpContentType(Enum):
    TEXT_HTML = 'text/html'
    APPLICATION_JSON = 'application/json'
    IMAGE_PNG = 'image/png'

@dataclass
class HTTPRequest:
    method: HTTPMethod
    url: str
    
def makeResponseHeader(status: HTTPStatusCode, contentType: HttpContentType, extra: dict|None = None) -> str:
    strResp = f'HTTP/1.1 {status.value[0]} {status.value[1]}\n'
    strResp += f'Content-Type: {contentType.value}\n'
    if extra:
        for key, value in extra.items():
            strResp += f'{key}: {value}\n'
    strResp += '\n'
    return strResp

def parseRequest(requests: str) -> HTTPRequest | None:
    if len(requests) < 1:
        return None
    arRequests = requests.split('\n')
    for line in arRequests:
        match = re.search(r'\b(GET|POST|DELETE|PUT|PATCH)\b\s+(.*?)\s+HTTP/1.1', line)
        if match:
            method = HTTPMethod(match.group(1))
            url = match.group(2)
            try:
                return HTTPRequest(method, url)
            except ValueError:
                return None
    return None

def getUserList():
    return [
        {'id': 1, 'name': 'Trump'},
        {'id': 2, 'name': 'Biden'},
        {'id': 3, 'name': 'Obama'},
    ]

def createServer():
    arPath = ['/', '/user/list', '/google.png', '/google']
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080))
        serverSocket.listen()
        while True:
            (connectionSocket, addr) = serverSocket.accept() # Blocking
            print('Connection received from ', addr)
            
            request = connectionSocket.recv(4096).decode('utf-8')
            print(request)
            req = parseRequest(request)
            if req is None or req.url is None:
                connectionSocket.shutdown(SHUT_WR)
                continue
            
            if req.url not in arPath:
                print('Resource not found')
                response = makeResponseHeader(HTTPStatusCode.NOT_FOUND, HttpContentType.TEXT_HTML)
                response += '<html><body>404 Not Found</body></html>\n'
                connectionSocket.sendall(response.encode('utf-8'))
                connectionSocket.shutdown(SHUT_WR)
                continue
            
            if req.url == '/google':
                response = makeResponseHeader(HTTPStatusCode.SEE_OTHER, HttpContentType.TEXT_HTML, {'Location': 'https://www.google.com'})
                connectionSocket.sendall(response.encode('utf-8'))
                connectionSocket.shutdown(SHUT_WR)
                continue
            
            response = ''
            if req.url == '/user/list':
                response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.APPLICATION_JSON)
                response += json.dumps(getUserList())
            elif req.url == '/':
                response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.TEXT_HTML)
                response += '<html><body>Hello World<br /><img src="/google.png" /></body></html>\n'
            elif req.url == '/google.png':
                response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.IMAGE_PNG)
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