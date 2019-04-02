import os
from base64 import b64encode
import json
import socket
import sys 
import base64
from time import sleep
tempData = bytearray()
BUFFER_SIZE=1024
# python clienttcp.py 127.0.0.1 1234 -u cat.png ->Para subir un archivo
def iniciar(ip,port,param,filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(10)
    s.connect((ip,int(port)))
    if param=="-u":
        currentPath =os.path.dirname(os.path.abspath(__file__)) + "\\filestosend\\"
        with open(currentPath + filename, "rb") as f:
            l = f.read()
        base64_bytes = b64encode(l)
        myFile = base64_bytes.decode("utf-8")
        data = {"filename": filename,"file": myFile,"param":param}
        dataToSend = json.dumps(data).encode("utf-8")
        s.sendall(dataToSend)
    elif  param=="-d":
        data = {"filename": filename,"param":param}
        dataToSend = json.dumps(data).encode("utf-8")
        s.sendall(dataToSend)
        result=s.recv(100000)
        print("result:"+result)
        print("Conecto con el socket")
        '''currentPath1 =os.path.dirname(os.path.abspath(__file__)) + "\\downloads\\"
        while True:
            dataReceived = s.recv(8042)
            print("Trajo respuesta",dataReceived)
            if dataReceived:#sys.getsizeof(dataReceived) > 17:
                tempData = tempData + dataReceived
            else:
                data = json.loads(tempData.decode("utf-8"))
                print(data)
                myFile = base64.b64decode(data["file"])
                with open(currentPath1 + data["filename"], "wb") as f:
                    f.write(myFile)
                    f.close()
                print("Descargo el archivo")
                break'''
    elif  param=="-l":
        data = {"param":param}
        dataToSend = json.dumps(data).encode("utf-8")
        print(dataToSend)
        s.send(b'nomames')
        result=s.recv(BUFFER_SIZE)
        print(result)
        print("Conecto con el socket")
        '''currentPath1 =os.path.dirname(os.path.abspath(__file__)) + "\\downloads\\"
        while True:
            dataReceived = s.recv(8042)
            print("Trajo respuesta",dataReceived)
            if dataReceived:#sys.getsizeof(dataReceived) > 17:
                tempData = tempData + dataReceived
            else:
                data = json.loads(tempData.decode("utf-8"))
                print(data)
                myFile = base64.b64decode(data["file"])
                with open(currentPath1 + data["filename"], "wb") as f:
                    f.write(myFile)
                    f.close()
                print("Descargo el archivo")
                break'''
    #s.close()
    
if __name__ == "__main__":
    if len(sys.argv)==5:
        iniciar(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else: 
        print("Debe digitar los argumentos correctmente")
