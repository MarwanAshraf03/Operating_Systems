import json
import math
import os
from random import random
from datetime import datetime
# to remove files from the actual OS
import shutil
# to deep copy an object
import copy
# from main import nameSpace

nameSpace = []

class leaf:
    """
    Changed the __init__ a little bit to accept initialization using
    a dictionary so that we can use the json objects to reload the leaf
    """
    def __init__(self, name=None, Type=None, partition=None, **argv):
        self.name = name
        self.type = Type
        self.access = '-rwx'
        self.path = 'root'
        self.partition = partition

        # create a unique id for each file in range of 1 to 9000
        self.getID()

        self.creationTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.modifyTime = self.creationTime
        self.accessTime = self.creationTime

        if Type == 'directory':
            self.children = []
            self.size = 0
        else:
            self.content = ''
            self.size = 0

        """
        This means that if argv is present use its values to initiate
        the leaf thus override those past assignments
        """
        # if argv is present use it to override the past assignments
        if argv:
            self.name = argv['Name']
            self.access = argv['Access']
            self.type = argv['type']
            self.Id = argv['ID']
            self.creationTime = argv['Created']
            self.accessTime = argv['Last accessed']
            self.modifyTime = argv['Modified']
            if self.type != 'directory':
                self.content = argv['content']
            if self.type == 'directory':
                self.children = argv['children']
            self.partition = argv['part']
            self.size = argv['size']
        if self.partition:
            self.totalSize = 1001
            self.size = 0
            self.block = 13

        nameSpace.append(self.Id)

    def getID(self):
        self.Id = math.ceil(random() * 9000)
        while self.Id in nameSpace:
            self.Id = math.ceil(random() * 9000)

    def updateSize(self):
        if self.type == 'directory':
            self.size = 0
            for i in self.children:
                self.size += i.size

    """
    This is a function to change the object to a dictionary representation
    """
    def dict(self):
        # if the leaf is a file
        if not self.partition and self.type != 'directory':
            return {"Access": f"{self.access}",
                    "ID": self.Id,
                    "type": f"{self.type}",
                    "Name": f"{self.name}",
                    "Created": self.creationTime,
                    "Last accessed": self.accessTime,
                    "Modified": self.modifyTime,
                    "path": self.path,
                    "content": self.content,
                    "part": self.partition,
                    "size": self.size
                }
        # if the leaf is a directory
        elif self.type == 'directory':
            return {"Access": f"{self.access}",
                    "ID": self.Id,
                    "type": f"{self.type}",
                    "Name": f"{self.name}",
                    "Created": self.creationTime,
                    "Last accessed": self.accessTime,
                    "Modified": self.modifyTime,
                    "path": self.path,
                    "part": self.partition,
                    "children": [],
                    "size": self.size,
                }

    # overwrite the print function
    def __str__(self):
        if self.type == 'directory':
            if self.partition:
                return f'Access: {self.access} -- ID: {self.Id} -- Name: {self.name} -- Total size: {self.totalSize} -- used space: {self.size} -- empty space: {self.totalSize - self.size} -- Created: {self.creationTime} -- Last accessed: {self.accessTime} -- Modified: {self.modifyTime}'
            else:
                return f'Access: {self.access} -- ID: {self.Id} -- Name: {self.name} -- Size: {self.size} -- Created: {self.creationTime} -- Last accessed: {self.accessTime} -- Modified: {self.modifyTime}'
        elif self.type != 'directory':
            return f'Acccess: {self.access} -- ID: {self.Id} -- Name: {self.name} -- Size: {self.size} -- Type: {self.type} -- Created: {self.creationTime} -- Last accessed: {self.accessTime} -- Modified: {self.modifyTime}'