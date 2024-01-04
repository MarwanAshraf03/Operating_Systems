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
import re

# Get the file type from its extension
def parseType(name):
    # locate the extension to set the file type
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

# a list of commands so we can avoid naming a file or a folder with one of them and to show the inforamtion about them
commands = {
    'mk':"if we're currently in a directory, it makes a new directory in it then asks for the name after you press ENTER. if we're in a file it appends new content to the file. (write mk, press enter then it will ask for the directory name or the file contnet, file content has no prompt)",
    'mkf':"if we're currently in a directory, it makes a new file in it then asks for the name after you press ENTER. if we're in a file it replaces the old file content with new one. (write mkf, press enter then it will ask for the file name or the file contnet, file content has no prompt)",
    'exit':"will stop the program (just write exit)",
    'ls':"if we're currently in a directory, it shows it's children's names. if we're currently in a file, it reads the file content (just type ls)",
    'ls -a':"shows the whole tree in a (just type ls -a)",
    '..':"takes you back to the parent directory of the current file/folder (just type ..)",
    'delete':"deletes a file/folder from your current directory. will ignore if we're currently in a file (type delete, press ENTER, it will ask for the name of the file to delete. if the file was created by the super user it will ask for a password which is FBI)",
    'copy':"if we're currently in a file, it will copy that file. if we're currently in a directory, it will ask for the name of the file/folder to copy (type copy, press ENTER, if it's a file it will copy it if it's a directory it will ask for the name of the file/folder to copy)",
    'cut':"if we're currently in a file, it mark that file to be moved. if we're currently in a directory, it will ask for the name of the file/folder to move (type cut, press ENTER, if it's a file it will makr it to move if it's a directory it will ask for the name of the file/folder to move)",
    'paste':"pastes the copied/moved object to the current directory (enter the directory where you wish to paste your file/folder, type paste)",
    'apply':"writes the tree to the real OS (just type apply)",
    'info':"returns some information about the file (enter the file/folder, type info)",
    'rename':"renames a file/folder (enter the file/folder you want to rename, type rename then press ENTER, type the new name)",
    'getsize':"returns size-related info about the file including blocks used (enter the file/folder, type getsize)",
    'search':"searches a directory for a give search (enter the directory you want to search in, type search then ENTER, enter the name of the search)"
}

# we only have one main partition (linux-like)
path = 'root'
# to track if the last operation was copy or cut
option = ''
# c will be the directory we're in
c = root.parsePath(path)
print('Type Help to open the list of commands')
print('Type Help + command to get further information about a command including how it works ')
while True:
    print(path + '>>', end=' ')
    # i is the command the user enters
    i = input()
    """
    creates directory if we're in a directory and writes content if we're in a file
    """
    if i == 'mk':
        # if the folder has the write access to it then go ahead
        if root.isWritable(c):
            # if it's a directory, add a new folder in it
            if c.type == 'directory':
                # ask for the new folder name
                name = input('Name: ')
                # check that it's not empty and is not in the list of commands
                if name.strip() == '' or name in commands.keys():
                    print("Name is not valid")
                else:
                    # add a new node and selt partition to False as it's just a directory
                    root.addChild(c, leaf(name, 'directory', False))
                    root.updatesize(root.root)
            # if it's a file append in its content
            else:
                # prompt the user to write the content of the file
                text = input('')
                # get old content
                content = root.getContent(c)
                # check if the new content is larger than the free space (we add one for the new line character)
                if (root.root.totalSize-root.root.size) < (len(text)+1) :
                    print("**Memory Full**")
                else:
                    # if the content is not empty then append the text to the old content separated by a new line
                    if content != '':
                        content += f'\n{text}'
                        root.updateContent(c, content)
                        # update file size
                        root.updatesize(root.root)
                    # if the content is empty they add the text to the file without appending the old content
                    else:
                        root.updateContent(c, text)
                        # update file size
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
                if name.strip() == ''  or name in commands.keys():
                    print("Name is not valid")
                else:
                    root.addChild(c, leaf(name, parseType(name), False))
                    root.updatesize(root.root)
            # if the leaf is a file the use the mkf to override the text in it
            else:
                # prompt the user to type the file content
                text = input('')
                # available space
                rs = (root.root.totalSize-root.root.size)
                # if new content is bigger than free space don't update
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
        # change the path
        path+=f'/{i}'
        # get the node from the path
        c = root.parsePath(path)
        path = c.path

    # returns a step back
    if i == '..' and path != 'root':
        path = path[:-len(c.name)-1]
        c = root.parsePath(path)
        path = c.path

    # deletes a provided file name from a the current directory
    if i == 'delete' and c.type == 'directory':
        if root.isWritable(c):
            # take file name as an input
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
            # copy the node not just get its address
            temp = copy.deepcopy(c)
            option = i

    # paste the copied or moved file
    if i == 'paste':
        if option == 'copy':
            root.copy(c, temp)
        if option == 'cut':
            root.cut(c, temp)

    # adds files to the real os and overwrites the last written tree
    if i == 'apply':
        # check if it exist before
        try:
            # remove the old files
            shutil.rmtree('root')
        except Exception as e:
            pass
        root.writeTree(root.root)

    # prints file/folder information
    if i == 'info':
        print(c)

    # rename file or folder
    if i=='rename':
        name=input('new name: ')
        #send the root node , current node and new name to rename function in tree class
        root.rename(root.root,c,name)
        #change the path of current node
        path = c.path
    
    # print size
    if i=='getsize':
        root.updatesize(root.root)
        # if current node is root print information about the root node because it's have more information like used space , free space ,used block etc
        if c.name=='root':
            print('size:1001 ',f'used space:{c.size} ',f'free space:{c.totalSize-c.size} ',f'used block:{c.size/c.block}')
        else:
        # if current node not root print the size of it and number of used block
             print(f'size:{c.size}',f'used block:{c.size / root.root.block}')

    # search in file
    if i=='search':
        name=input('File name: ')
        # send the file or folder name to search function in tree class
        root.search(c,name)   

    if i == 'Help' :
        print('\n'.join(commands.keys()))
    
    if re.match(r'Help ([a-zA-Z]+)+',i):
        command = i[i.find(' ')+1:]
        if command in commands.keys():
            print(f'{command}: {commands[command]}')
        else:
            print('unkown command')

    root.updatesize(root.root)
    root.submit()
