import socket
from concurrent.futures import ThreadPoolExecutor
import sys,os

import Utility
from Utility import getListOfFiles,saveFile, createDirectory,getListOfFiles,createFileListForUser,renameFile
from time import sleep

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
IP1 = None
IP2 = None
IP3 = None
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
FILESERVER_1_PORT = 5000
FILESERVER_2_PORT = 6000
FILESERVER_3_PORT = 7000
replicaAddresses = []
FILESERVER_1_ADDR = (IP1, FILESERVER_1_PORT)
FILESERVER_2_ADDR = (IP2, FILESERVER_2_PORT)
FILESERVER_3_ADDR = (IP3, FILESERVER_3_PORT)

THREAD_POOL_SIZE = 10000
CREATE_DIRECTORY = "CREATE_DIRECTORY"
DELETE_DIRECTORY = "DELETE_DIRECTORY"
DELETE_FILE = "DELETE_FILE"
CREATE_FILE = "CREATE_FILE"
GET_CURRENT_PERMISSION = "GET_CURRENT_PERMISSION"
SET_PERMISSION = "SET_PERMISSION"
PATH_PREFIX = "FileServer"
SUCCESS = "SUCCESS"
COMMIT = "COMMIT"
ABORT = "ABORT"
NO_OF_REPLICAS = 3


def phaseOne(ADDR, clientName: str, filePath: str, fileData: str):
    replicaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    replicaSocket.connect(ADDR)

    replicaSocket.send("ONE".encode(FORMAT))
    status = replicaSocket.recv(SIZE).decode(FORMAT)

    replicaSocket.send(clientName.encode(FORMAT))
    status = replicaSocket.recv(SIZE).decode(FORMAT)

    replicaSocket.send(filePath.encode(FORMAT))
    status = replicaSocket.recv(SIZE).decode(FORMAT)

    replicaSocket.send(fileData.encode(FORMAT))
    status = replicaSocket.recv(SIZE).decode(FORMAT)  # Should contain success

    replicaSocket.close()
    if status == SUCCESS:
        return True
    else:
        return False

def phaseTwo(clientName: str,ADDR, action: str):
    replicaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    replicaSocket.connect(ADDR)

    replicaSocket.send("ONE".encode(FORMAT))
    status = replicaSocket.recv(SIZE).decode(FORMAT)

    replicaSocket.send(clientName.encode(FORMAT))
    status = replicaSocket.recv(SIZE).decode(FORMAT)

    replicaSocket.send(action.encode(FORMAT))
    status = replicaSocket.recv(SIZE).decode(FORMAT)

    replicaSocket.close()

    return status


def showAllFiles(conn, clientName):
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"{clientName} - Msg from client :  {msg}.")
    try:
        listOfAllFiles = getListOfFiles(os.path.join(PATH_PREFIX,clientName))
        print(listOfAllFiles)
    except:
        print("Error")
    print(createFileListForUser(listOfAllFiles,clientName,PATH_PREFIX))
    conn.send(str(createFileListForUser(listOfAllFiles,clientName,PATH_PREFIX)).encode(FORMAT))
    conn.close()
    return True


def createFile(conn, clientName):
    print("Trigger2")
    filename = conn.recv(SIZE).decode(FORMAT)
    conn.send("Filename received.".encode(FORMAT))
    print(f"{clientName} - [RECV] Receiving the filename. {filename}")


    data = conn.recv(SIZE).decode(FORMAT)
    conn.send("File data received".encode(FORMAT))
    print(f"{clientName} - [RECV] Receiving the file data. {data}")

    #TODO Implement 2PC and server replication below

    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"{clientName} - [RECV] Msg. {msg}")
    saveFile(clientName, filename, data,PATH_PREFIX)
    conn.send("Transaction Done".encode(FORMAT))
    conn.close()
    print(f"{clientName} - [DISCONNECTED] {addr} disconnected.")

    pass

def readFile(conn,clientName):
    filePath = conn.recv(SIZE).decode(FORMAT)
    print(f"{clientName} - File to read :  {filePath}.")
    basePath = os.path.join(PATH_PREFIX,clientName)
    flag, data = Utility.readFile(os.path.join(basePath,filePath))

    if flag:
        print(data)
        conn.send(data.encode(FORMAT))
    else:
        conn.send("FILE NOT FOUND".encode(FORMAT))
    conn.close()
    return True

def updateFileName(conn,clientName):
    oldfilePath = conn.recv(SIZE).decode(FORMAT)
    conn.send("Received".encode(FORMAT))
    print(f"{clientName} - Old File Path :  {oldfilePath}.")
    basePath = os.path.join(PATH_PREFIX, clientName)
    newFilePath = conn.recv(SIZE).decode(FORMAT)

    flag = renameFile(os.path.join(basePath,oldfilePath),os.path.join(basePath,newFilePath))

    if flag:
        conn.send("FILE RENAMED SUCCESSFULLY".encode(FORMAT))
    else:
        conn.send("FILE NOT FOUND".encode(FORMAT))
    conn.close()
    return True


def deleteFile(conn, clientName):
    filePath = conn.recv(SIZE).decode(FORMAT)
    print(f"{clientName} - Old File Path :  {filePath}.")
    basePath = os.path.join(PATH_PREFIX, clientName)

    flag = Utility.deleteFile(os.path.join(basePath, filePath))

    if flag:
        conn.send("FILE DELETED SUCCESSFULLY".encode(FORMAT))
    else:
        conn.send("FILE NOT FOUND".encode(FORMAT))
    conn.close()
    return True


def createDir(conn, clientName):
    dirPath = conn.recv(SIZE).decode(FORMAT)
    print(f"{clientName} - DirPAth :  {dirPath}.")
    basePath = os.path.join(PATH_PREFIX, clientName)

    flag,message = Utility.createDirectory(os.path.join(basePath, dirPath))

    if flag:
        conn.send(message.encode(FORMAT))
    else:
        conn.send(message.encode(FORMAT))
    conn.close()
    return True


def concurrentFunction(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    clientName = conn.recv(SIZE).decode(FORMAT)
    conn.send("ClientName received.".encode(FORMAT))
    print(f"{clientName} - [RECV] Received the client name.")

    createDirectory(os.path.join(PATH_PREFIX,clientName))

    command = conn.recv(SIZE).decode(FORMAT)
    conn.send("Command received.".encode(FORMAT))
    print(f"{clientName} - [RECV] Received the command {command}.")

    if command == "show":
        showAllFiles(conn,clientName)
    if command == "createFile":
        print("Trigger1")
        createFile(conn,clientName)
    if command == "readFile":
        readFile(conn,clientName)
    if command == "updateFileName":
        updateFileName(conn,clientName)
    # if command == "updateFileContent":
    #     updateFileContent(conn,clientName)
    if command == "deleteFile":
        deleteFile(conn,clientName)
    if command == "createDir":
        createDir(conn,clientName)
    # if command == "deleteDir":
    #     deleteDir(conn,clientName)


    return True


if __name__ == "__main__":
    IP1 = sys.argv[1]  # Replica 1 Address
    IP2 = sys.argv[2]  # Replica 2 Host
    IP2 = sys.argv[3]  # Replica 3 Host

    for i in [1, 3, 5]:
        replicaAddresses.append((sys.argv[i], int(sys.argv[i + 1])))

    print(replicaAddresses)
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. 
        Bind the IP and PORT to the server. 
        Server is listening, i.e., server is now waiting for the client to connected. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)

    server.listen(1000)
    print("[LISTENING] Server is listening.")

    threadPoolExecutor = ThreadPoolExecutor(THREAD_POOL_SIZE)

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        threadPoolExecutor.submit(concurrentFunction, conn, addr)
