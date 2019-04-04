import socket,select
import json
import os
import sys
import base64
from base64 import b64encode
from time import sleep
currentPath = os.path.dirname(os.path.abspath(__file__)) + "\\files\\"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 5005))
s.listen(5)
print("socket is listening")
tempData = bytearray()
def RealizarPeticionUpfile(data):
    myFile = base64.b64decode(data["file"])
    with open(currentPath + data["filename"], "wb") as f:
        f.write(myFile)
        f.close()
def downloadFile(c,data1):
    print("Entro a descargar")
    currentPath1 = os.path.dirname(os.path.abspath(__file__)) + "\\files\\"
    with open(currentPath1 + data1["filename"], "rb") as f:
        l = f.read()
    base64_bytes = b64encode(l)
    myFile = base64_bytes.decode("utf-8")
    data1 = {"filename": data1["filename"], "file": myFile}
    dataToSend = json.dumps(data1).encode("utf-8")
    c.sendall(dataToSend)
    print("Envio para el cliente")
    #print(dataToSend)
def getListFiles(c):
    lista=os.listdir(os.path.dirname(os.path.abspath(__file__)) + "\\files\\")
    js = {"list": lista}
    dataToSend = json.dumps(js).encode("utf-8")
    c.send(dataToSend)
    print(dataToSend)
while True:
    conn, addr = s.accept()
    tempData=bytearray()
    while True:
        ready = select.select([conn], [], [], 1)
        print("esperando mensaje")
        if ready[0]:
            print(ready[0])
            print("Entramos denuevo")
            dataReceived = conn.recv(4096)
            if dataReceived:
                print("recibido")
                print(dataReceived)
                tempData +=dataReceived
                try:
                    data = json.loads(tempData.decode("utf-8"))
                    if data["param"] =="-u":
                        RealizarPeticionUpfile(data)
                        break
                    elif data["param"] =="-d":
                        downloadFile(conn,data)
                        break 
                    elif data["param"] =="-l":
                        getListFiles(conn)
                        break
                except:
                    continue
                