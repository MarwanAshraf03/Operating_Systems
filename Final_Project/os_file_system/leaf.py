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
        self.access = 'rwx'
        self.path = 'root'
        self.partition = partition

        # create a unique id for each file in range of 1 to 9000
        #TODO maybe change namespace to a static var
        self.getID()

        self.creationTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.modifyTime = self.creationTime
        self.accessTime = self.creationTime

        if Type == 'directory':
            self.children = []
        else:
            self.content = ''
            self.size = 0

        """
        This means that if argv is present use its values to initiate
        the leaf thus override those past assignments
        """
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
        if self.partition:
            self.size = 1001
            self.block = 13

        nameSpace.append(self.Id)

    def getID(self):
        self.Id = math.ceil(random() * 9000)
        while self.Id in nameSpace:
            self.Id = math.ceil(random() * 9000)

    """
    This is a function to change the object to a dictionary representation
    """
    def dict(self):
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
                    "part": self.partition
                }
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
                    "children": []
                }

    # overwrite the print function
    def __str__(self):
        if self.partition:
            return f'ID: {self.Id} -- Name: {self.name} -- Size: {self.size}'
        elif self.type != 'directory':
            return f'Access: {self.access} -- ID: {self.Id} -- Type: {self.type} -- Name: {self.name} -- Created: {self.creationTime} -- Last accessed: {self.accessTime} -- Modified: {self.modifyTime}'
        else:
            return f'ID: {self.Id} -- Name: {self.name} -- Created: {self.creationTime} -- Last accessed: {self.accessTime} -- Modified: {self.modifyTime}'
