#! /usr/bin/env python3
import sys
sys.path.append("../lib")
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        while True:
    
            payload = framedReceive(sock, debug)
            if not payload:
                break
            
            if debug: print("rec'd: ", payload)
            totalFile += payload.decode()
            
        ##### in case file did not exist on client side
        if not fileName:
            sys.exit()

        ##### checks if file already exists, adds a number to the name if yes
        repeatCounter = 0
        decodedName = fileName.decode()
        filesInDir = os.listdir(os.getcwd())
        while True:
            ##### got this if statement from "Harwee" on stackoverflow
            if decodedName in filesInDir:
                print ("reapeat")
                repeatCounter += 1
                splitName = re.split("\.", decodedName)
                if (repeatCounter > 1):
                    splitName[0] = splitName[0][:-1]
                decodedName = (splitName[0] + ("%d." % repeatCounter) + splitName[1]) 
            else:
                file = open(decodedName, 'w')
                break
                
        file.write(totalFile)
        
        file.close()
            
