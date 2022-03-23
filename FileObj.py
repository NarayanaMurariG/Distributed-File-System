class FileObj:
    filePath = None
    fileData = None

    # default constructor
    def __init__(self, filePath, fileData):
        self.filePath = filePath
        self.fileData = fileData

    def getFilePath(self):
        return self.filePath

    def getFileData(self):
        return self.fileData
