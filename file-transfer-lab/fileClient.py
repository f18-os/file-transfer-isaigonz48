#! /usr/bin/env python3

# Echo client program
import os, socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

os.write(1, ("Name of file: ").encode())
fileName = os.read(0,1024)

##### Will make sure that the file name doesn't contain new lines or spaces
while (re.search('\n',fileName.decode()) != None):
    decodedName = fileName.decode()
    if decodedName == '':
       os.write(2,("File does not exist\n").encode)
       sys.exit()
    elif decodedName[0] == ' ':
        fileName = fileName[1:]
    elif decodedName[-1] == ' ' or decodedName[-1] == '\n':
        fileName = fileName[:-1]

if fileName == '':
    os.write(2,("File does not exist\n").encode)
    sys.exit()

##### Attempt to open file
try:
    file = open(fileName.decode(),'r')
except FileNotFoundError:
    os.write(2, ("File does not exist\n").encode())
    sys.exit()

##### Sends the file name first so that server knows what to save as
framedSend(s,fileName,debug)

print (os.environ['PATH'])
##### Will send file 100 bytes at a time
file = open(fileName,'r')
while True:
    fileText = file.read(100)
    ##### breaks loop at end of file
    if not fileText:
        break
    #print("sending at most 100 bytes")
    framedSend(s, fileText.encode(), debug)

file.close()
