Sending/Receiving Files Lab

* fileClient.py will ask user for input of the name of the file that you want to send

* fileServer.py will receive the file and put its contents into a new file called "RECEIVE[sent file name]"
** This was done to avoid confusion in what file was sent and what file was received

* fileServer.py supports multiple clients

* fileClient.py and fileServer.py use  framedSock.py to frame the messages

* fileClient.py and fileServer.py use a lot of code from framedClient.py and framedServer.py