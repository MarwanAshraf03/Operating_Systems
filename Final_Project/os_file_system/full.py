import re
# to retrieve saved files
import json
import math
# to add the tree in the real OS
import os
from random import random
from datetime import datetime
# to remove files from the actual OS
import shutil
# to deep copy an object
import copy
from turtle import update

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















class tree:
    """
    Modify a little in the __init__ function to accept initialization
    using a dictionary representation
    """
    def __init__(self, **dict):
        # if the dict is present use it to initialize the root
        if dict:
            self.root = leaf(**dict)
        # if the dict is not present initialize the root normally
        else:
            # we set the root of the tree and give it name, type, and the boolean set to true meaning it is a partition not a normal directory
            self.root = leaf('root', 'directory', True)
            # default access for the root
            self.root.access = 'srwx'

    """
    Add file/folder to a directory
    """
    def addChild(self, Dir, leaf):
        # check if the name exists before creating new file/folder
        if leaf.name in self.ls(Dir):
            print('Duplicated name')
            return

        # changing the path of the new file to be present in the directory and creating it
        leaf.path = Dir.path + f'/{leaf.name}'
        Dir.children.append(leaf)

    # check if the permissions are entered as read, write, execute. Also a user cannot write if they can't read the file
    def validAccess(self, a):
        if len(a)!=3 or a[0] not in ['r', '-'] or a[1] not in ['w', '-'] or a[2] not in ['x', '-']:
            return False
        return True

    """
    return the names of files/folders in a directory or the content in a file
    """    
    def ls(self, leaf):
        # if it is a file return its content
        if leaf.type !='directory':
            return leaf.content

        # if it's a directory make a list of names
        names = []
        # iterate children and add each child's name
        for x in leaf.children:
            names.append(x.name)
        return names

    """
    get the file/folder with the path given
    """
    def parsePath(self, path):
        # change path to a list of steps,  if a step (directory) not found then the path is wrong
        path = path.split('/')
        # we always start from root so remove it as we know already
        path.remove('root')
        # var root will be our iterator
        root = self.root
        # when we open a file/folder we must change its access time
        root.accessTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for x in path:
            # catch an error if the file/folder not found and returning the last available folder in the path
            try:
                # search for the name of the file in the list of names returned by ls(), if found return its index to use in the children list
                root = root.children[self.ls(root).index(x)]
                # we accessed the file/folder so we need to update access time
                root.accessTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except:
                print('Invalid path')
                # if we failed, we return the last available node in the path
                return root
        # we return the node
        return root

    """
    check if we have write permission in a node
    """
    def isWritable(self, f):
        if f.access[2] == 'w':
            return True
        return False

    """
    print the tree in the console
    """
    def showTree(self, node):
        # we add spaces before file name = the depth of the file (number of folders before it) to create a hierarchy view
        print(' '*(len(node.path.split('/'))-1)*2, node.name)
        # if it's a directory we recursively do the same for its children
        if node.type == 'directory':
            for x in node.children:
                self.showTree(x)

    """
    writes the files in the real OS
    """
    def writeTree(self, node):
        # if it's a directory we add to the real os using its path (note: its path to the os is relative to our project directory but everything is wrapped in the root directory)
        if node.type == 'directory':
            os.makedirs(node.path)
            # recursively iterate through children and apply the function
            for x in node.children:
                self.writeTree(x)
        else:
            # if it's a text file we create the file and add its content to it
            if node.type == 'text file':
                # create the file and open it in write mode
                with open(node.path, 'w') as f:
                    # add its content
                    f.write(node.content)
            else:
                # if it's not a text file we do the same but without adding its content because we assumend all contents is text and that's not the case in real files
                with open(node.path, 'w') as f:
                    f.write('')

    """
    deletes file/folder
    """
    def delete(self, Dir, name):
        # if the file is found we execute the function
        if name in self.ls(Dir):
            # if the file is created by the super user, we ask for the password to delete
            if Dir.access[0] == 's':
                pas = input('Enter Super User Password: ')
                # if passwords don't match, don't delete the file
                if pas != 'FBI':
                    print('Wrong password')
                    return
            # if the function wasn't stopped due to any of the above conditions then we delete the file and change its directory modification time
            Dir.children.pop(self.ls(Dir).index(name))
            Dir.modifyTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            # if the file name we provided doesn't exist tell the user
            print('File does not exist')
            return


    def changeAccess(self, file, access):
        # check again if the entered access is the way we parse it
        if self.validAccess(access[1:]):
            file.access = access
        else:
            print('Wrong access')
            return

    def getAccess(self, file):
        return file.access

    """
    pastes a copied object
    """
    def copy(self, Dir, file):
        # get the root to change its size after copying a file (because we created a new file that might have content)
        root = self.parsePath('root')
        # if the file size is bigger than free space, we abort the paste because there is no space
        if root.totalSize-root.size < file.size:
            print('No enough space')
            return
        # we can't paste a file/directory inside a file as it has no children
        if Dir.type != 'directory':
            print('operation not possible in a file')
        else:
            # if name already exist, change to a new name (copy_old name), keep doing that until it's unique and paste it
            while file.name in self.ls(Dir):
                file.name = 'copy_'+file.name
            # paste the copy
            self.addChild(Dir, file)
            # get current date
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # directory has been modified so change its modification time
            Dir.modifyTime = now
            # that's a new file so a new creation time and the modification and access times will initially be the same as creationg
            file.createTime = now
            file.modifyTime = now
            file.accessTime = now
            # that's a new file, so a new path and new ID as well
            self.updatePath(Dir,file,'copy')

    """
    Updates the path of a file after pasting
    """
    def updatePath(self,Dir,f,o):
        # the file path is the same as the directory + the file name
        f.path = Dir.path+'/'+f.name
        # if the operation is a copy so we create a new ID as it's a new file
        if o == 'copy':
            # getID() creates new unique ID
            f.getID()
            # if the pasted node was a directory, recursively update children paths and IDs
            if f.type == 'directory':
                for x in f.children:
                    self.updatePath(f,x,'copy')
        else:
            # if the operation wasn't a copy so so we recursively update children paths only
            if f.type == 'directory':
                for x in f.children:
                    self.updatePath(f,x,'cut')

    """
    same as copy function but it asks the user if the want to overwrite the file instead of changing the name
    """
    def cut(self, Dir, file):
        if Dir.type != 'directory':
            print('operation not possible')
        else:
            if Dir.path == file.path[:file.path.rfind('/')]:
                print("can't move to the same directory")
                return
            # if the file name exist, ask the user if they want to overwrite the old file
            if file.name in self.ls(Dir):
                r = input('File already exist,  overwrite? (Y|N): ')
                if r == 'Y':
                    Dir.children.remove(Dir.children[self.ls(Dir).index(file.name)])
                else:
                    return
            # the old directory where the file/folder came from
            old = self.parsePath(file.path[:file.path.rfind('/')])
            # remove the file/folder from its old directory
            old.children.remove(old.children[self.ls(old).index(file.name)])
            # add the file to the new directory
            self.addChild(Dir, file)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Dir.modifyTime = now
            file.createTime = now
            file.modifyTime = now
            file.accessTime = now
            self.updatePath(Dir,file,'cut')

    def getContent(self, file):
        return file.content

    """
    update content of a file
    """
    def updateContent(self, file, text):
        file.content = text
        # update the modification time and file size
        file.modifyTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.size = len(file.content)

    """
    update size of desk
    """
    def updatesize(self,node):
        # if the node is a directory, its size will be the sum of its children sizes
       if node.type == 'directory':
           # if it has children we recursively iterate them
            if len(node.children) > 0:
                # the total size
                total=[]
                # for each child
                for x in node.children:
                    # we add its size and its children sizes
                    total.append(self.updatesize(x))
                    # the directory is the sum of all sizes
                    node.size=sum(total)
                return node.size    
            else:
                # if it has no children, its size is 0
                node.size=0
                return 0   
        # if it's a file, its size is its content length
       else:
            node.size = len(node.content)
            return node.size


    """
    Renames a file/directory
    """
    def rename(self,root,node,name):
        # we can't use root as a name
        if name=='root':
            print('you can\'t use root as a name')
            return
        # if the node is the root, we can't change its name
        if root==node:
            print('you can\'t change the name of root')
            return
        # here we use recursive way to get the names of folder or directory in same level to chek that we will not duplicate the name
        for x in root.children:
            if x.path == node.path:
                # if there is another dir or file with the same name we stop the function
                if name in self.ls(root):
                    print('there is another directory with the same name')        
                    return
                # if not we rename the file and then update the path of that
                node.name=name
                self.updatePath(root,node,'o')
                return
            else:
                if x.path in node.path:
                    self.rename(x,node,name) 
    
    """
    search function
    """
    def search(self,node,name):
        # we take the current node and chek if it's directory and has children we will search in the child of it 
        if node.type == 'directory':
            if len(node.children) > 0:
                for x in node.children:
                    self.search(x,name)
            else:
                pass
        # if not we will check if it's have same name we search about 
        if node.name==name:
            print(node.path)                

    """
    a method that recursively generate the dictionary representation of the program 
    """
    def dict(self, node=None):
        # the initial empty dictionary
        dictt = {}
        # check if the node of dict() is none then we create the root as a key and list of its information and children
        if node == None:
            # create list of root's children
            dictt[self.root.name] = self.root.children.copy()
            # add root's information at the 0 index
            dictt[self.root.name].insert(0, self.root.dict())
            # iterates over root's children starting from index 1 to avoid iteration over root's information
            for i in range(1, len(dictt[self.root.name])):
                # if this child is directory call the dict() method on it
                if dictt[self.root.name][i].type == 'directory':
                    dictt[self.root.name][i] = self.dict(dictt[self.root.name][i])
                # if this child is file add its string as a child to this index
                else:
                    dictt[self.root.name][i] = json.dumps(dictt[self.root.name][i].dict())
        # if the node of dict() is not none then we create this node as a key and list of its information and children
        else:
            # create list of node's children
            dictt[node.name] = node.children.copy()
            # add node's information at the 0 index
            dictt[node.name].insert(0, node.dict())
            # iterates over node's children starting from index 1 to avoid iteration over node's information
            for i in range(1, len(dictt[node.name])):
                # if this child is directory call the dict() method on it
                if dictt[node.name][i].type == 'directory':
                    dictt[node.name][i] = self.dict(dictt[node.name][i])
                # if this child is file add its string as a child to this index
                else:
                    dictt[node.name][i] = json.dumps(dictt[node.name][i].dict())
        # return the dictionary and this is the system's dictionary representation used to retrieve the last state
        #   of the code
        return dictt

    """
    This is used to save the program dictionary representation to 'file.json'
    in a json format
    """
    def submit(self):
        # writes the dictionary of the system to the file.json
        with open('file.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.dict()))

    """
    A method to return the dictionary representation of this instance
    in a string form
    """
    def __str__(self):
        # returns string of the dictionary of the system
        return str(self.dict())

    """
    A method that is called if there is a json file found in the working directory
    and it calls the self.load() method with the 'root' as a path and the list that
    has root's information
    """
    def load_system(self):
        # retrieve the dictionary from 'file.json'
        with open('file.json', 'r', encoding='utf-8') as f:
            dict = json.load(f)
        # calls the self.load method using the root as a path and the list of root
        self.load('root', dict['root'])        
    
    """
    A method that is called by self.load_system() it is used to recursively iterate through
    the root's list of information and if it finds a file it attaches it to the current directory
    and if it finds a directory it creates it then use its information to build it.
    """
    def load(self, path, lst):
        # a loop to iterate through the list of items 
        for i in range(1, len(lst)):
            # if the list item is string then it is a file so add it to the node as a file child
            if type(lst[i]).__name__ == 'str':
                # create a new leaf using the variable expansion to create the leaf with existing leaf's information
                self.addChild(self.parsePath(path), leaf(**json.loads(lst[i])))
            # if the list item is not a string then it is a directory so add it to the node as a folder child
            #   then call the self.load method on it
            else:
                # create a new leaf using the variable expansion to create the leaf with existing leaf's information
                nleaf = leaf(**lst[i][list(lst[i].keys())[0]][0])
                # add the leaf to the current node as a child
                self.addChild(self.parsePath(path), nleaf)
                # call the self.load method using this leaf's information
                self.load(nleaf.path, lst[i][list(lst[i].keys())[0]])
























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
    'ls':"if we're currently in a directory, it shows its children's names. if we're currently in a file, it reads the file content (just type ls)",
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
print("""
The code creates a 'file.json' when you type exit, if you run the code again the code
continues from where you left it with all the directories and file you created.
To go to a certain directory just type its name.
""")
print('Type Help to open the list of commands')
print('Type Help + command to get further information about a command including how it works ')
while True:
    print("\nType directory's name to navigate to it")
    print("-----------------------------------------")
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