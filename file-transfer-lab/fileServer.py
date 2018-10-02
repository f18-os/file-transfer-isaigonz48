#! /usr/bin/env python3
import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    #print("connection rec'd from", addr)


    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("child handling stuff form")

        totalFile = ""
        newLineCounter = 0
        fileName = framedReceive(sock, debug)

        while True:
    
            payload = framedReceive(sock, debug)
            if newLineCounter == 1:
                if debug: print("rec'd: ", payload)
                totalFile += payload.decode()
                if makeNewLine == 1:
                    totalFile += '\n'
                    newLineCounter = 0
            else:
                if not payload:
                    break
                if payload.decode() == "YES":
                    makeNewLine = 1
                newLineCounter = 1

        if not fileName:
            sys.exit()
        file = open(("RECEIVED" + fileName.decode()), 'w')

        file.write(totalFile)
        
        file.close()

