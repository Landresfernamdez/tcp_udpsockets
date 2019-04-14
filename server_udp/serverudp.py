import socket,select
import json
import os
import sys
import base64
from base64 import b64encode
from time import sleep
import platform
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Get the local host name
myHostName = socket.gethostname()
print("Name of the localhost is {}".format(myHostName))
# Get the IP address of the local host
myIP = socket.gethostbyname(myHostName)
print("My Ip is:"+myIP)
s.bind((myIP, 5005))
print("socket is listening")
tempData = bytearray()
def RealizarPeticionUpfile(data):
    carpetafiles=""
    if platform.system()=='Windows':
        carpetafiles="\\files\\"
    if platform.system()=='Linux':
        carpetafiles="/files/"
    currentPath = os.path.dirname(os.path.abspath(__file__)) + carpetafiles
    myFile = base64.b64decode(data["file"])
    with open(currentPath + data["filename"], "wb") as f:
        f.write(myFile)
        f.close()
def downloadFile(c,data1,addr):
    carpetafiles=""
    if platform.system()=='Windows':
        carpetafiles="\\files\\"
    if platform.system()=='Linux':
        carpetafiles="/files/"
    currentPath1 = os.path.dirname(os.path.abspath(__file__)) + carpetafiles
    with open(currentPath1 + data1["filename"], "rb") as f:
        l = f.read()
    base64_bytes = b64encode(l)
    myFile = base64_bytes.decode("utf-8")
    data1 = {"filename": data1["filename"], "file": myFile}
    dataToSend = json.dumps(data1).encode("utf-8")
    for i in range(0, len(dataToSend), 2):
        dt = dataToSend[i:i+2]
        c.sendto(dt,addr)
    print("Envio para el cliente")
def getListFiles(c,addr):
    carpetafiles=""
    if platform.system()=='Windows':
        carpetafiles="\\files\\"
    if platform.system()=='Linux':
        carpetafiles="/files/"
    lista=os.listdir(os.path.dirname(os.path.abspath(__file__)) + carpetafiles)
    js = {"list": lista}
    dataToSend = json.dumps(js).encode("utf-8")
    c.sendto(dataToSend,addr)
while True:
    tempData=bytearray()
    while True:
        ready = select.select([s], [], [], 1)
        if ready[0]:
            dataReceived,addrees = s.recvfrom(51200)
            if dataReceived:
                tempData +=dataReceived
                try:
                    data = json.loads(tempData.decode("utf-8"))
                    if data["param"] =="-u":
                        RealizarPeticionUpfile(data)
                        break
                    elif data["param"] =="-d":
                        downloadFile(s,data,addrees)
                        break 
                    elif data["param"] =="-l":
                        getListFiles(s,addrees)
                        break
                except:
                    continue
