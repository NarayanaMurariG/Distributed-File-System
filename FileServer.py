import os.path
from concurrent.futures import ThreadPoolExecutor
import socket
import sys
from Utility import deleteFile
import threading, queue
import FileObj

IP = socket.gethostbyname(socket.gethostname())
SIZE = 1024
FORMAT = "utf-8"
THREAD_POOL_SIZE = 10000
COMMIT = "COMMIT"
ABORT = "ABORT"
SUCCESS = "SUCCESS"
jobQueue = queue.Queue()
isolatedStorage = {}

# def phaseOne(conn, addr, pathPrefix, logPrefix):
#     print(f"{logPrefix} [NEW CONNECTION] {addr} connected.")
#     """ Receiving the filename and data from the client. """
#     try:
#         userName = conn.recv(SIZE).decode(FORMAT)
#         filename = conn.recv(SIZE).decode(FORMAT)
#         data = conn.recv(SIZE).decode(FORMAT)
#         print(f"{logPrefix} [RECV] Receiving the filename and data")
#         filePath = pathPrefix + "/" + filename
#         fileObject = FileObj(filePath,data)
#         isolatedStorage.update(userName,fileObject)
#         conn.send(SUCCESS.encode(FORMAT))
#     except:
#         conn.send(ABORT.encode(FORMAT))
#
#     conn.close()
#     """ Closing the connection from the client. """
#     print(f"{logPrefix} [DISCONNECTED] {addr} disconnected.")
#     return True

# def phaseTwo(conn, addr, pathPrefix, logPrefix):
#     print(f"{logPrefix} [NEW CONNECTION] {addr} connected.")
#     """ Receiving the filename and data from the client. """
#     try:
#         userName = conn.recv(SIZE).decode(FORMAT)
#         message = conn.recv(SIZE).decode(FORMAT)
#
#         if message == COMMIT:
#             fileObj = isolatedStorage.get(userName)
#             file = open(fileObj.getFilePath(), "w")
#             file.write(fileObj.getFileData())
#             file.close()
#
#         isolatedStorage.pop(userName)
#         conn.send(SUCCESS.encode(FORMAT))
#     except:
#         conn.send(ABORT.encode(FORMAT))
#
#     conn.close()
#     """ Closing the connection from the client. """
#     print(f"{logPrefix} [DISCONNECTED] {addr} disconnected.")
#     return True


def concurrentFunction(conn, addr, pathPrefix, logPrefix):
    print(f"{logPrefix} [NEW CONNECTION] {addr} connected.")
    """ Receiving the filename from the client. """
    try:
        phaseType = conn.recv(SIZE).decode(FORMAT)
        conn.send("Gotcha".encode(FORMAT))
        print(f"{logPrefix} [RECV] {phaseType}")
        if phaseType == "ONE":
            userName = conn.recv(SIZE).decode(FORMAT)
            conn.send("Gotcha".encode(FORMAT))
            filename = conn.recv(SIZE).decode(FORMAT)
            conn.send("Gotcha".encode(FORMAT))
            data = conn.recv(SIZE).decode(FORMAT)

            print(f"{logPrefix} [RECV] Receiving the filename and data")
            filePath = pathPrefix + "/" + filename
            fileObject = FileObj(filePath, data)
            isolatedStorage.update(userName, fileObject)

            conn.send(SUCCESS.encode(FORMAT))
        else:
            userName = conn.recv(SIZE).decode(FORMAT)
            conn.send("Gotcha".encode(FORMAT))
            message = conn.recv(SIZE).decode(FORMAT)

            if message == COMMIT:
                fileObj = isolatedStorage.get(userName)
                file = open(fileObj.getFilePath(), "w")
                file.write(fileObj.getFileData())
                file.close()
                conn.send(SUCCESS.encode(FORMAT))
            else:
                conn.send("ABORTED".encode(FORMAT))
            isolatedStorage.pop(userName)

            conn.close()
    except:
        conn.close()
        print("Error occoured in thread")

    return True


def startServer(portNumber):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (IP, portNumber)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)

    server.listen(10000)
    print(f"[LISTENING] Server is listening on {ADDR}.")
    return server


def initaliseCache(pathPrefix):
    cacheFile = os.path.join(pathPrefix + "/UserCache.csv")
    deleteFile(cacheFile)
    file = open(cacheFile, 'w')
    file.close()


if __name__ == "__main__":
    replicaNo = int(sys.argv[1]) #Replica No
    portNumber = int(sys.argv[2]) #PortNumber
    pathPrefix = sys.argv[3] #FileServerName

    initaliseCache(pathPrefix)
    server = startServer(portNumber)

    threadPoolExecutor = ThreadPoolExecutor(THREAD_POOL_SIZE)

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"Received a connection from {addr}")
        threadPoolExecutor.submit(concurrentFunction, conn, addr, pathPrefix, replicaNo)
