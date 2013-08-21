import socket

s=socket.socket()
s.bind(('192.168.1.182',8009))
s.listen(5)

while 1:
    cs,address = s.accept()
    #print 'server:got connected from:\n',address
    #data = raw_input()
    #cs.send(data)
    ra=cs.recv(512)
    print "server:",ra
cs.close()
