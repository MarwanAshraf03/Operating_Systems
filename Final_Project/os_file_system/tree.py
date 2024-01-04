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
from leaf import leaf

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
            # if name already exist, change to a new name (copy_old name) and paste it
            if file.name in self.ls(Dir):
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
