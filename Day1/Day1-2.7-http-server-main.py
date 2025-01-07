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

def getUserList() -> None:
    return [
        {'id': 1, 'name': 'Trump'},
        {'id': 2, 'name': 'Biden'},
        {'id': 3, 'name': 'Obama'},
    ]

# /
def handler_home(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.TEXT_HTML)
    response += '<html><body>Hello World<br /><img src="/google.png" /></body></html>\n'
    return response.encode('utf-8')

# /user/list
def handler_user_list(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.APPLICATION_JSON)
    response += json.dumps(getUserList())
    return response.encode('utf-8')

# /google
def handler_google(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.SEE_OTHER, HttpContentType.TEXT_HTML, {'Location': 'https://www.google.com'})
    return response.encode('utf-8')

# /google.png
def handler_google_png(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.OK, HttpContentType.IMAGE_PNG).encode('utf-8')
    with open('google.png', 'rb') as f:
        response += f.read()
    return response

def hander_404(request: HTTPRequest) -> bytes:
    response = makeResponseHeader(HTTPStatusCode.NOT_FOUND, HttpContentType.TEXT_HTML)
    response += '<html><body>404 Not Found</body></html>\n'
    return response.encode('utf-8')

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
            
            resp = None
            if req.url not in arPath:
                resp = hander_404(req)
            elif req.url == '/google':
                resp = handler_google(req)
            elif req.url == '/user/list':
                resp = handler_user_list(req)
            elif req.url == '/':
                resp = handler_home(req)
            elif req.url == '/google.png':
                resp = handler_google_png(req)
            
            if resp is not None:
                chunk_size = 1024
                arChunks = [resp[i:i+chunk_size] for i in range(0, len(resp), chunk_size)]
                for chunk in arChunks:
                    connectionSocket.sendall(chunk)
            connectionSocket.shutdown(SHUT_WR)
            
    except KeyboardInterrupt:
        print('\nShutting down the server\n')
        serverSocket.close()
    except Exception as e:
        print('Unexpected error:', e)
        
if __name__ == '__main__':
    createServer()