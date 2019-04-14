import os
from base64 import b64encode
import json
import socket,select
import sys 
import base64
from time import sleep
import platform
#tempData = bytearray()
BUFFER_SIZE=1024
# python clienttcp.py 127.0.0.1 5005 -u cat.png ->Para subir un archivo
def iniciar(ip,port,param,filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(10)
    s.connect((ip,int(port)))
    if param=="-u":
        carpetafilestosend=""
        if platform.system()=='Windows':
            carpetafilestosend="\\filestosend\\"
        if platform.system()=='Linux':
            carpetafilestosend="/filestosend/"
        currentPath =os.path.dirname(os.path.abspath(__file__)) +carpetafilestosend
        with open(currentPath + filename, "rb") as f:
            l = f.read()
        base64_bytes = b64encode(l)
        myFile = base64_bytes.decode("utf-8")
        data = {"filename": filename,"file": myFile,"param":param}
        dataToSend = json.dumps(data).encode("utf-8")
        s.sendall(dataToSend)
    elif  param=="-d":
        tempData = bytearray()
        carpetafilesdownloads=""
        if platform.system()=='Windows':
            carpetafilesdownloads="\\downloads\\"
        if platform.system()=='Linux':
            carpetafilesdownloads="/downloads/"
        currentPath1 =os.path.dirname(os.path.abspath(__file__)) + carpetafilesdownloads
        data = {"filename": filename,"param":param}
        dataToSend = json.dumps(data).encode("utf-8")
        s.sendall(dataToSend)
        while True:
            ready = select.select([s], [], [], 1)
            if ready[0]:
                dataReceived = s.recv(4096)
                try:
                    if dataReceived:#sys.getsizeof(dataReceived) > 17:
                        tempData = tempData + dataReceived
                    data = json.loads(tempData.decode("utf-8"))
                    myFile = base64.b64decode(data["file"])
                    with open(currentPath1 + data["filename"], "wb") as f:
                        f.write(myFile)
                        f.close()
                    break
                except:
                    continue
        s.close()
                    
    elif  param=="-l":
        tempData = bytearray()
        data = {"param":param}
        dataToSend = json.dumps(data).encode("utf-8")
        s.send(dataToSend)
        while True:
            ready = select.select([s], [], [], 1)
            if ready[0]:
                dataReceived = s.recv(4096)
                try:
                    if dataReceived:
                        tempData = tempData + dataReceived
                        data = json.loads(tempData.decode("utf-8"))
                        print("El archivo cuenta con :",data["list"])
                        break
                except:
                    continue
        s.close()
    
if __name__ == "__main__":
    if len(sys.argv)==5:
        iniciar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else: 
	print("Debe digitar los argumentos correctamente")


