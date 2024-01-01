import json
import math
import os
from random import random
from datetime import datetime
# to remove files from the actual OS
import shutil
# to deep copy an object
import copy
from tree import tree
from leaf import leaf

# Get the file type from its extension
def parseType(name):
    extension = name[name.rfind('.')+1:]
    if extension == 'txt':
        return 'text file'
    if extension in ['jpg', 'jpeg', 'png']:
        return 'image'
    if extension == 'mp3':
        return 'audio file'
    if extension == 'mp4':
        return 'video'
    return 'File'
if os.path.exists('file.json'):
    with open('file.json', 'r') as f:
        dict = json.load(f)
    root = tree(**dict['root'][0])
    root.load_system()
else:
    root = tree()
# we only have one main partition (linux-like)
path = 'root'
# to track if the last operation was copy or cut
option = ''
# c will be the directory we're in
c = root.parsePath(path)
while True:
    print(path + '>>', end=' ')
    i = input()
    # creates directory if we're in a directory and writes content if we're in a file
    if i == 'mk':
        if root.isWritable(c):
            if c.type == 'directory':
                name = input('Name: ')
                root.addChild(c, leaf(name, 'directory', False))
            else:
                root.updateContent(c)
        else:
            print('Access denied')

    # creates file if we're in a directory and writes content if we're in a file
    if i == 'mkf':
        if root.isWritable(c):
            if c.type == 'directory':
                name = input('Name: ')
                root.addChild(c, leaf(name, parseType(name), False))
            else:
                root.updateContent(c)
        else:
            print('Access denied')

    if i == 'exit':
        break

    # lists current directory direct children
    if i == 'ls':
        print(root.ls(c))

    # lists all the tree
    if i == 'ls -a':
        root.showTree(root.root)

    # if the user entered a directory or file name in our current directory, we open it. we reset path so if an error happened the parsePath method returns the last available path
    if i in root.ls(c):
        path+=f'/{i}'
        c = root.parsePath(path)
        path = c.path

    # returns a step back
    if i == '..' and path != 'root':
        path = path[:-len(c.name)-1]
        c = root.parsePath(path)
        path = c.path

    # deletes a provided file name from a the current directory
    if i == 'delete':
        if root.isWritable(c):
            name = input("Name: ")
            root.delete(c, name)
        else:
            print('Acess denied')
    
    # changes access, if it's no more writable we take a step back
    if i == '-p':
        root.changeAccess(c, input('New_Access: '))
        if c.access[0] == '-':
            path = path[:-len(c.name)-1]
            c = root.parsePath(path)
            path = c.path

    # we take a temporary object from our copied, cut files
    if i in ['copy', 'cut']:
        name = input('File name: ')
        if name not in root.ls(c):
            print('File not found')
        else:
            # deep copy the file so when we change it,  we don't affect the original file
            temp = copy.deepcopy(root.parsePath(f'{path}/{name}'))
            option = i

    if i == 'paste':
        if option == 'copy':
            root.copy(c, temp)
        if option == 'cut':
            root.cut(c, temp)

    # adds files to the real os and overwrites the last written tree
    if i == 'apply':
        try:
            shutil.rmtree('root')
        except Exception as e:
            pass
        root.writeTree(root.root)

    # returns file/folder info
    if i == 'info':
        print(c)

    if i == 'mm':
        print(root)
    
    root.submit()
