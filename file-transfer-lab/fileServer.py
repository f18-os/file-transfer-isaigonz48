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

    ##### Child forked
    if not os.fork():

        totalFile = ""
        fileName = framedReceive(sock, debug)
        #### makeNewLine is a flag for whether or not the line ends with '\n'
        makeNewLine = 0
        while True:
    
            payload = framedReceive(sock, debug)
            if not payload:
                break
            ##### turn on makeNewLine flag and receive the line of the file
            if payload.decode() == "YES":
                makeNewLine = 1
                payload = framedReceive(sock, debug)

            if debug: print("rec'd: ", payload)
            totalFile += payload.decode()
            ##### append '\n' to end of the line
            if makeNewLine == 1:
                totalFile += '\n'
                makeNewLine = 0

        ##### in case file did not exist on client side
        if not fileName:
            sys.exit()
        file = open(("RECEIVED" + fileName.decode()), 'w')

        file.write(totalFile)
        
        file.close()

