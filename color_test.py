

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8080
byt = '33333333'.encode()
s.connect(('192.168.2.97', port))
for i in range(50):
    msg = '33333333'
    num = int(msg, 16)
    byt += msg.encode('utf-8')
print(byt)
s.send(byt)


