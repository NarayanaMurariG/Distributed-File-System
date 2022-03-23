import os
import csv
import sys


def createDirectory(path):
    try:
        if os.path.isdir(path):
            return False,"Directory Already Exists"
        else:
            os.mkdir(path)
            return True,"Directory created successfully"
    except:
        print("Error in creating directory")
        return False,"Improper Path Construction"


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def deleteFile(path):
    if os.path.isfile(path):
        os.remove(path)
        return True
    else:
        return False

def deleteDirectory(path):
    if os.path.isdir(path):
        os.rmdir(path)
        return True
    else:
        return False

def createFileListForUser(list: list,clientName: str,pathPrefix):
    newList = []
    for str in list:
        newList.append(str.replace(os.path.join(pathPrefix,clientName),''))
    return newList


def renameFile(path,newPath):
    if os.path.isfile(path):
        os.rename(path,newPath)
        return True
    else:
        return False

def readFile(path):
    if os.path.isfile(path):
        file = open(path, "r")
        data = file.read()
        return True,data
    else:
        return False,None

def shareFile(path,sharedBy,sharedWith):
    return None


def checkIfUserNameExists(newUserName):
    userNames = []
    if newUserName in userNames:
        return True
    else:
        return False

def authenticateUser(userName,hashedPassword):
    hashedPasswordFromDB = "getHashedPasswordForUser(userName)"
    if hashedPasswordFromDB == hashedPassword:
        return True
    else:
        return False

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    if len(allFiles) == 0:
        allFiles.append(dirName)
    return allFiles

def saveFile(clientName,filePath,fileData,pathPrefix):

    absolutePath = None
    if sys.platform.startswith('win'):
        absolutePath = pathPrefix + "\\" + clientName + "\\" + filePath
    else:
        absolutePath = pathPrefix + "/" + clientName + "/" + filePath

    print(f"{clientName} {absolutePath}")
    if os.path.isfile(absolutePath):
        return False,"File Already Exists"
    try:
        file = open(absolutePath, "w")
        file.write(fileData)
        file.close()
    except:
        print(f"{clientName} {absolutePath} Error")
        return False,"Incorrect path formation"
    print(f"{clientName} {absolutePath} saved")
    return True,"File Save Successful"


if __name__ == "__main__":
    output = getAllFilesList("FileServer1")
    print(output)
    print(createDirectory("FileServer11"))


