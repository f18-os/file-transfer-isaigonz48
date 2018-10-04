Sending/Receiving Files Lab

* fileClient.py will ask user for input of the name of the file that you want to send

* fileServer.py will receive the file and put its contents into a file with the sent files names
** fileServer.py adds a number to the file name if the original name already exosted

* fileServer.py supports multiple clients

* fileClient.py and fileServer.py use framedSock.py to frame the messages

* fileClient.py only sends 100 byes at a time

* fileClient.py and fileServer.py use code from framedClient.py, framedServer.py, and framedForkServer.py

* Got os.listdir and the if statement for checking if the file is in the directory from "Harwee" on stackoverflow