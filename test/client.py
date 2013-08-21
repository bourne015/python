import socket

#s=socket.socket()
#s.connect(('192.168.1.182',8007))   
#data=s.recv(512)
#print 'client:the data received is\n    ',data
#s.send('hihi I am client')

sock2 = socket.socket()
sock2.connect(('192.168.1.182',8007))
while 1:
    #data2=sock2.recv(512)
    #print 'client:received from server is:\n   ',data2
    data = raw_input()
    sock2.send(data)
sock2.close()
