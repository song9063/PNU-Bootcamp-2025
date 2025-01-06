import socket

cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliSocket.connect(('localhost', 8080))

strCmd = '''GET / HTTP/1.1
Host: localhost:8080

'''.encode()
cliSocket.send(strCmd)

while True:
    response = cliSocket.recv(1024)
    if not response or len(response) < 1:
        break
    print(response.decode(), end='')
    
cliSocket.close()