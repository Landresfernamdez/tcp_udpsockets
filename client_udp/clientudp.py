import os
from base64 import b64encode
import json
import socket
import select
import sys
import base64
from time import sleep
#tempData = bytearray()
BUFFER_SIZE = 51200
# python clientudp.py 127.0.0.1 5002 -u cat.png ->Para subir un archivo

def iniciar(ip, port, param, filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.settimeout(2)
    if param == "-u":
        currentPath = os.path.dirname(
            os.path.abspath(__file__)) + "\\filestosend\\"
        with open(currentPath + filename, "rb") as f:
            l = f.read()
        base64_bytes = b64encode(l)
        myFile = base64_bytes.decode("utf-8")
        data = {"filename": filename, "file": myFile, "param": param}
        dataToSend = json.dumps(data).encode("utf-8")
        for i in range(0, len(dataToSend), 2):
            dt = dataToSend[i:i+2]
            s.sendto(dt, (ip, int(port)))
        print("prueba:", sys.getsizeof(dataToSend), "type:", type(dataToSend))

    elif param == "-d":
        tempData = bytearray()
        currentPath1 = os.path.dirname(
            os.path.abspath(__file__)) + "\\downloads\\"
        data = {"filename": filename, "param": param}
        ds = json.dumps(data).encode("utf-8")
        s.sendto(ds,(ip, int(port)))
        while True:
            print("Espera mensaje")
            ready = select.select([s], [], [], 1)
            if ready[0]:
                dataReceived,adress  = s.recvfrom(BUFFER_SIZE)
                print("Llego mensaje")
                print(dataReceived)
                try:
                    if dataReceived:  # sys.getsizeof(dataReceived) > 17:
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
    elif param == "-l":
        tempData = bytearray()
        data = {"param": param}
        dataToSend = json.dumps(data).encode("utf-8")
        '''listaPaquetes=[]
        contador=0
        for i in range(0, len(dataToSend), 2):
            listaPaquetes.append(dataToSend[i:i+2])
            contador=contador+1'''
        s.sendto(dataToSend, (ip, int(port)))
        while True:
            print("Entro aqui")
            ready = select.select([s], [], [], 1)
            if ready[0]:
                dataReceived,addres = s.recvfrom(4096)
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
    if len(sys.argv) == 5:
        iniciar(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Debe digitar los argumentos correctmente")
