# This python file uses the os module to traverse & get information from a directory. Object oriented programming is used to create & dynamically traverse a directory.

import os  # operating system library
from os import path as p


class Directory:

    path = ""
    visited = []
    visitedf = []
    individuals = []
    depth = 0
    breadth = 0
    trees = []
    cleaned = []

    def __init__(self):
        pass

    # Setup, Update & Formatting Functions

    def setup(self):
        self.path = p.dirname(p.abspath(__file__))
        self.formatpath()
        os.chdir(self.path)

    def update(self, path=""):
        if p.exists(path) and len(path) > 0:
            self.path += "/" + path
            os.chdir(path)
            self.depth += 1
        else:
            os.chdir("..")
            self.path = os.getcwd()
            self.depth -= 1
        self.formatpath()
        self.converttotree(iscomplex=True, p=False)

    def getpath(self):
        self.formatpath()
        return self.path

    def formatpath(self):
        self.path = self.path.replace(chr(92), chr(47))

    def converttotree(self, iscomplex=False, p=False, manualpath=""):
        tree = self.getpath().split(
            sep="/") if len(manualpath) == 0 else manualpath.split(sep="/")
        if iscomplex:
            if len(self.trees) == 0:
                self.trees.append(tree)
                if p:
                    print(self.trees)
            else:
                temptree = []
                treex = self.trees[-1]
                for folder in tree:
                    if folder not in treex:
                        temptree.append(folder)
                self.cleaned.append(temptree)
                if tree not in self.trees:
                    self.trees.append(tree)
                    if p:
                        print("Full Tree: {ft}\n\nUnique Tree: {ut}".format(
                            ft=self.trees, ut=self.cleaned))
        return tree

    def cuttree(self, n=1, manualpath=""):
        return self.converttotree(iscomplex=True, manualpath=manualpath)[:len(self.converttotree()) - n + 1]

    def createpath(self, n=1, manualtree=[]):
        tree = self.cuttree(n) if len(manualtree) == 0 else manualtree
        path = ""
        symbol = ""
        for i in range(len(tree)):
            symbol = "/" if i < len(tree) - 1 else ""
            folder = tree[i]
            path += "{f}{s}".format(f=folder, s=symbol)
        return path

    def tail(self, n=1, manualpath=""):
        return self.cuttree(n=n, manualpath="")[-1]

    # Visited Functions

    def getvisited(self):
        return self.visited

    def wasvisited(self):
        return self.getpath() in self.getvisited()

    def markvisited(self):
        self.tracefolder()
        if not self.wasvisited():
            self.visited.append(self.getpath())
            self.visitedf.append(self.tail())
            self.converttotree(iscomplex=True)
            print("{p} -V".format(p=self.getpath()))

    def tracefolder(self):
        folder = self.tail()
        if folder not in self.individuals:
            self.individuals.append(folder)

    def getindividualfolders(self):
        return self.individuals

    def logged(self, folder):
        return folder in self.getindividualfolders()

    # Boundary Checking

    def flist(self, path=""):
        temppath = self.getpath()
        if len(path) > 0 and p.exists(path):
            temppath += "/" + path
        alllist = os.listdir(temppath)
        for folder in alllist:
            if (not p.isdir(folder)) or (not folder.endswith("__")):
                alllist.remove(folder)
        return alllist

    def nflist(self, n=1):
        path = self.createpath(n=n)
        folders = os.listdir(path)
        for folder in folders:
            if (not p.isdir(folder)) or (p.isfile(folder)) or (folder.endswith("__")):
                folders.remove(folder)
        return folders

    def size(self, path=""):
        return len(self.flist(path=path))

    def nsize(self, n=1):
        return len(self.nflist(n=n))

    def sizevisited(self, path=""):
        folders = self.flist(path=path)
        tempfolders = []
        for visit in self.visited:
            for folder in folders:
                if (folder in visit) and (folder not in tempfolders):
                    tempfolders.append(folder)
        return len(tempfolders)

    def sizeunvisited(self, path=""):
        return self.size(path) - self.sizevisited(path) if self.size(path) > 0 else 0

    def nsizeunvisited(self, n=1):
        return self.nsize(n) - self.nsizevisited(n) if self.nsize(n) > 0 else 0

    def nsizevisited(self, n=1):
        folders = self.nflist(n=n)
        tempfolders = []
        for visit in self.visited:
            for folder in folders:
                if (folder in visit) and (folder not in tempfolders):
                    tempfolders.append(folder)
        return len(tempfolders)

    def visitdifference(self, path=""):
        return self.size(path) - self.sizevisited(path)

    def nvisitdifference(self, n=1):
        return self.nsize(n) - self.nsizevisited(n)

    def cf(self, prt=5, command=""):
        symbol = ": " if len(command) > 0 else ""
        folder = self.flist()[self.breadth] if self.size(
        ) > 0 else self.tail(1)
        size = self.size(folder)
        self.tracefolder()
        if prt == 1:
            print("{c}{s}{f}, size = {n}".format(
                c=command, s=symbol, f=folder, n=size))
        elif prt == 2:
            print("{c}{s}{f}, size = {n}".format(c=command, s=symbol,
                  f=self.getindividualfolders(), n=size))
        elif prt == 3:
            print("{c}{s}{f}, size = {n}".format(
                c=command, s=symbol, f=self.flist(), n=size))
        elif prt == 4:
            print("{c}{s}{f}, size = {n}".format(c=command, s=symbol,
                  f=self.getpath(), n=size))
        return folder

    def has(self, v=False):
        cf = self.cf()
        criteria1 = self.size(cf) > 0
        criteria2 = self.visitdifference(cf) > 0
        return criteria2 if v else criteria1

    def end(self, v=False):
        return not self.has(v)

    def beginning(self, v=False):
        criteria1 = self.depth == 1
        criteria2 = self.nvisitdifference(2) > 0
        return (criteria1 and criteria2) if v else criteria1

    def lowest(self):
        return self.breadth >= self.nsize(2)

    def highest(self):
        return self.breadth == 0

    def fullyvisited(self):
        return self.nvisitdifference(2) == 0

    # Traversal

    def forward(self, v=False, rep=True, stopcondition=False, down=True):
        cf = self.cf()
        if rep:
            cf = self.cf(4, "Forward")
        if not self.end(v):
            self.update(cf)
            if not rep:
                cf = self.cf(4, "Forward")
            if rep and not stopcondition:
                self.forward(v, rep)
        else:
            if down:
                self.down()

    def down(self):
        if not self.lowest():
            self.breadth += 1
            self.cf(1, "Down")

    def up(self):
        if not self.highest():
            self.breadth -= 1
            self.cf(1, "Up")


direc = Directory()
direc.setup()
direc.forward()
