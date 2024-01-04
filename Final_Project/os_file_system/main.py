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
# if the 'file.json' is present
if os.path.exists('file.json'):
    # retrieve the dictionary of the system
    with open('file.json', 'r') as f:
        dict = json.load(f)
    # initialize the root tree with the root's information
    root = tree(**dict['root'][0])
    # call the load_system method of the root tree
    root.load_system()
    # call the updatesize method of the root tree to get the latest size of the root
    root.updatesize(root.root)
# if the 'file.json' is not present
else:
    # initialize the root tree without any thing
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
    """
    creates directory if we're in a directory and writes content if we're in a file
    """
    if i == 'mk':
        # if the folder has the write access to it then go ahead
        if root.isWritable(c):
            if c.type == 'directory':
                name = input('Name: ')
                if name.strip() == '':
                    print("Name is not valid")
                else:
                    root.addChild(c, leaf(name, 'directory', False))
                    root.updatesize(root.root)
            else:
                # prompt the user to write the content of the file
                text = input('')
                content = root.getContent(c)
                # TODO: explain the size management
                if (root.root.totalSize-root.root.size) < (len(text)+1) :
                    print("**Memory Full**")
                else:
                    # if the content is not empty then append the text to the old content separated by a new line
                    if content != '':
                        content += f'\n{text}'
                        root.updateContent(c, content)
                        root.updatesize(root.root)
                    # if the content is empty they add the text to the file without appending the old content
                    else:
                        root.updateContent(c, text)
                        root.updatesize(root.root)
        # if the folder is not writable
        else:
            # print access denied
            print('Access denied')

    # creates file if we're in a directory and writes content if we're in a file
    if i == 'mkf':
        # checks if the leaf has the write access to it
        if root.isWritable(c):
            if c.type == 'directory':
                name = input('Name: ')
                if name.strip() == '':
                    print("Name is not valid")
                else:
                    root.addChild(c, leaf(name, parseType(name), False))
                    root.updatesize(root.root)
            # if the leaf is a file the use the mkf to override the text in it
            else:
                # prompt the user to type the file content
                text = input('')
                # TODO: explain the size management
                rs = (root.root.totalSize-root.root.size)
                if (rs < len(text)) and (len(text) > len(root.getContent(c))):
                    print("**Memory Full**")
                # update the content of the file
                else:
                    root.updateContent(c, text)
                    root.updatesize(root.root)
        # if not print access denied
        else:
            print('Access denied')

    if i == 'exit':
        break

    """
    lists current directory direct children
    """
    if i == 'ls':
        # if the current leaf is readable go ahead
        if root.getAccess(c)[1] == 'r':
            print(root.ls(c))
        # if the current leaf is not readable deny access
        else:
            print('Access Denied')

    """
    lists all the tree
    """
    if i == 'ls -a':
        # if the current leaf is readable go ahead
        if (root.getAccess(root.parsePath('root'))[1] == 'r') and (root.getAccess(c)[1] == 'r'):
            root.showTree(root.root)
        # if the current leaf is not readable deny access
        else:
            print('Access Denied')

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
    
    """
    change permissions
    """
    if i == 'permission':
        # if the access of leaf is not set by a super user
        if c.access[0] == '-':
            # prompt user to give new access
            access = input('New_Access: ')
            # change leaf's access with user's new access
            root.changeAccess(c, '-'+access)
        # if the access of leaf is set by a super user
        else:
            # prompt user to give the super user's password which is 'FBI'
            password = input('Enter Super User Password: ')
            # if password is correct
            if password == 'FBI':
                # prompt user to give new access
                access = input('New_Access: ')
                # change leaf's access with user's new access
                #  and add '-' to the start of user's access
                #  to indicate that this permission is set with
                #  the normal permission command
                root.changeAccess(c, '-'+access)
            # if password is not correct
            else:
                # say 'wrong password'
                print('Wrong Password')
        # if c.access[0] == '-':
        #     path = path[:-len(c.name)-1]
        #     c = root.parsePath(path)
        #     path = c.path

    """
    change permissions using the privilage of a super user
    """
    if i == 'sudo permission':
        # prompt the user to type the password which is 'FBI'
        password = input('Enter Super User Password: ')
        # if password is correct
        if password == 'FBI':
            # prompt the user with the new access
            access = input('New_Access: ')
            # change the access of current leaf to user's access
            #  add an 's' to the start of the user's access to indicate
            #  that this permission is set with 'sudo'
            root.changeAccess(c, 's'+access)
        # if password is not correct
        else:
            # say 'wrong password'
            print('Wrong Password')
        # if c.access[0] == '-':
        #     path = path[:-len(c.name)-1]
        #     c = root.parsePath(path)
        #     path = c.path

    # we take a temporary object from our copied, cut files
    if i in ['copy', 'cut']:
        if c.type == 'directory':
            name = input('File name: ')
            if name not in root.ls(c):
                print('File not found')
            else:
                # deep copy the file so when we change it,  we don't affect the original file
                temp = copy.deepcopy(root.parsePath(f'{path}/{name}'))
                option = i
        else:
            temp = copy.deepcopy(c)
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

    # prints file/folder information
    if i == 'info':
        print(c)

    # rename file
    if i=='rename':
        name=input('new name: ')
        root.rename(root.root,c,name)
        path = c.path
    
    # print size
    if i=='getsize':
        root.updatesize(root.root)
        if c.name=='root':
            print('size:1001 ',f'used space:{c.size} ',f'free space:{c.totalSize-c.size} ',f'used block:{c.size/c.block}')
        else:
             print(f'size:{c.size}',f'used block:{c.size / root.root.block}')

    # search in file
    if i=='search':
        name=input('File name: ')
        root.search(c,name)    

    root.updatesize(root.root)
    #root.updateSize(root.parsePath('root'))
    root.submit()
