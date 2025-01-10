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
    path: str
    query: dict = None

def parseQuery(url: str) -> tuple[str, dict | None]:
    # (\/[\w\-.\/]*)+([/#]*)([0-9a-zA-Z\-]*)\?*(.*)
    # https://regexr.com/
    path = url
    query = {}
    match = re.search(r'(\/[\w\-.\/]*)+([/#]*)([0-9a-zA-Z\-]*)\?*(.*)', url)
    if match:
        print(len(match.groups()))
        path = match.group(1)
        if path[-1] == '/':
            path = path[:-1]
        if path == '':
            path = '/'
        queryStr = match.group(4)
        for q in queryStr.split('&'):
            arQs = q.split('=')
            if len(arQs) == 2:
                query[arQs[0]] = arQs[1]
    return path, query

def parseRequest(requests: str) -> HTTPRequest | None:
    if len(requests) < 1:
        return None
    arRequests = requests.split('\n')
    for line in arRequests:
        match = re.search(r'\b(GET|POST|DELETE|PUT|PATCH)\b\s+(.*?)\s+HTTP/1.1', line)
        if match:
            method = HTTPMethod(match.group(1))
            url = match.group(2)
            path, query = parseQuery(url)
            try:
                return HTTPRequest(method, url, path, query)
            except ValueError:
                return None
    return None

def makeResponseHeader(status: HTTPStatusCode, contentType: HttpContentType, extra: dict|None = None) -> str:
    strResp = f'HTTP/1.1 {status.value[0]} {status.value[1]}\n'
    strResp += f'Content-Type: {contentType.value}\n'
    if extra:
        for key, value in extra.items():
            strResp += f'{key}: {value}\n'
    strResp += '\n'
    return strResp

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

def handle_request(request: HTTPRequest) -> bytes:
    resp = None
    print(f'Handle request: {request.path}')
    if request.path == '/google':
        resp = handler_google(request)
    elif request.path == '/user/list':
        resp = handler_user_list(request)
    elif request.path == '/':
        resp = handler_home(request)
    elif request.path == '/google.png':
        resp = handler_google_png(request)
    else:
        resp = hander_404(request)
    return resp
    

def createServer():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080))
        serverSocket.listen()
        while True:
            (connectionSocket, addr) = serverSocket.accept() # Blocking
            print('Connection received from ', addr)
            
            request = connectionSocket.recv(4096).decode('utf-8')
            # print(request)
            req = parseRequest(request)
            if req is None or req.url is None:
                connectionSocket.shutdown(SHUT_WR)
                continue
            
            resp = handle_request(req)
            
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