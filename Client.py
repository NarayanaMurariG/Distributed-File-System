import socket,sys
from os import system

# IP = "10.0.0.18"  # socket.gethostbyname(socket.gethostname())
IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024



def authenticateUser(userName: str, password: str):
    # compute password hash and send across network
    # If authenticated proceed else exit
    authenticated = True
    return authenticated


def printUserGuide():
    print("show : Show all my files")
    print("createFile filePath : Create file from filePath")
    print("createDir dirPath : Create directory from dirPath")
    print("deleteFile filePath : Delete file from filePath")
    print("updateFileName oldFilePath newFilePath : To update fileName")
    print("updateFileContent filePath : Update Content of file from filePath")
    print("readFile filePath : To readFilePath")
    print("help : To see guide again")
    print("clear : To clear console output")
    print("exit : To quit")

def printAllFiles(listAsStr: str):
    listAsStr = listAsStr[1:len(listAsStr)-1]
    print("Below are your files")
    print("----------------------------------")
    list = listAsStr.split(', ')
    for str in list:
        print(str[2:len(str)-1])
    print("----------------------------------")


def showAllFiles(clientName):
    # TODO
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    """ Sending the clientName to the server. """
    client.send(clientName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the Command to the server. """
    client.send(command.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send("Get My Files".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    # print(f"[SERVER]: {msg}")
    printAllFiles(msg)
    client.close()
    return True

def createFile(command: str,clientName,filePath):
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)

    """ Opening and reading the file data. """
    file = open(filePath, "r")
    data = file.read()

    """ Sending the clientName to the server. """
    client.send(clientName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the Command to the server. """
    client.send(command.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the filename to the server. """
    client.send(filePath.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the file data to the server. """
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send("Waiting on Status".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    """ Closing the file. """
    file.close()

    """ Closing the connection from the server. """
    client.close()
    return True


def readFile(command,clientName,filePath):
    # TODO
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    """ Sending the clientName to the server. """
    client.send(clientName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the Command to the server. """
    client.send(command.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send(filePath.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[FileName]: {filePath}")
    print(f"[FileData]: {msg}")

    client.close()
    return True


def updateFileName(command, clientName, oldFilePath, newFilePath):
    # TODO
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    """ Sending the clientName to the server. """
    client.send(clientName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the Command to the server. """
    client.send(command.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send(oldFilePath.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)

    client.send(newFilePath.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.close()
    return True


def updateFileContent():
    # TODO
    print("TODO")
    pass


def deleteFile(command,clientName,filePath):
    # TODO
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    """ Sending the clientName to the server. """
    client.send(clientName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the Command to the server. """
    client.send(command.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send(filePath.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.close()
    return True


def createDir(command,clientName,directoryPath):
    # TODO
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    """ Sending the clientName to the server. """
    client.send(clientName.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    """ Sending the Command to the server. """
    client.send(command.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.send(directoryPath.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    client.close()
    return True


def deleteDir():
    # TODO
    print("TODO")
    pass


if __name__ == '__main__':
    print('Welcome to Distributed File System')
    fileName = "fasak1.txt"

    userName = input("Enter your username : ")

    if (authenticateUser(userName,"password") == False):
        print("Incorrect UserName, try again later.")
    else:
        printUserGuide()
        while True:
            print("Enter your command : ")
            command = input("cmd : ")
            args = command.split(" ")
            if args[0] == "show":
                showAllFiles(userName)
            if args[0] == "help":
                printUserGuide()
            if args[0] == "createFile": #createFile filePath
                createFile(args[0],userName,args[1])
            if args[0] == "readFile": #createFile filepath
                readFile(args[0],userName,args[1])
            if args[0] == "updateFileName": #updateFileName oldName newName
                updateFileName(args[0],userName,args[1],args[2])
            if args[0] == "updateFileContent":
                updateFileContent()
            if args[0] == "deleteFile": #deleteFile filepath
                deleteFile(args[0],userName,args[1])
            if args[0] == "createDir": #createDir dirPath
                createDir(args[0],userName,args[1])
            if args[0] == "deleteDir": #deleteDir dirPath
                deleteDir()
            if args[0] == "exit":
                sys.exit()
            if args[0] == "clear":
                if sys.platform.startswith('win'):
                    _ = system('cls')
                else:
                    _ = system('clear')

    # saveFile("Client1", fileName)