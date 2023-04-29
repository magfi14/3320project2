# Use the OS, Simple Colors & Datetime modules to explore an existing set of directories in a Python directory.

import os
import simple_colors as s
from os import path as p
import datetime as dt


def println(string):

    # Prints a new line after the string by using the \n ASCII character in print(string).

    print("{s}\n".format(s=string))


class printformatter:

    # A class that contains methods to print strings in different colors.

    def __init__(self):
        pass

    def printf(self, string, color="black", px=False, newline=True):

        # Prints a string in a specified color.

        thingtoprint = string
        if color == "black":
            thingtoprint = s.black(string)
        elif color == "blue":
            thingtoprint = s.blue(string)
        elif color == "green":
            thingtoprint = s.green(string)
        elif color == "magenta":
            thingtoprint = s.magenta(string)
        elif color == "red":
            thingtoprint = s.red(string)
        elif color == "yellow":
            thingtoprint = s.yellow(string)
        elif color == "cyan":
            thingtoprint = s.cyan(string)
        elif color == "white":
            thingtoprint = s.white(string)
        elif color == "pink":
            thingtoprint = s.pink(string)
        if px:
            if not newline:
                print(thingtoprint)
            else:
                println(thingtoprint)
        return thingtoprint

    def perror(self, string):

        # Prints a string in red, italicized.

        return self.printf("\033[1m\x1b[3m{string}\033[0m\x1b[0m".format(string=string), "red", px=True)


class directory:

    # A class that contains methods to explore a directory.

    curpath = ""
    deep = 0
    index = 0
    foldersvisited = []
    pathsvisited = []
    pf = None
    origpath = ""
    logtext = ""

    def __init__(self):

        # Initializes the directory class.

        self.addtolog("Start\n", "-" * 50)
        self.pf = printformatter()

    def addtolog(self, prompt, result):

        # Adds a line to the log file if the current directory is the original directory, otherwise stored in a backend array to populate into the file later.

        time = dt.datetime.now().strftime("%H:%M:%S")
        self.tick = True
        logline = "\n{t} | {p} | {r}\n{line}\n".format(
            t=time, p=prompt.upper(), r=result, line="~" * 50)
        self.logtext += str(logline)
        if self.curpath == self.origpath:
            with open("log.txt", "w") as file:
                for line in self.logtext.split(sep="\n"):
                    file.write(line + "\n")
                file.close()

    def setpath(self):

        # Sets the current directory to the directory of the file.

        self.curpath = p.dirname(p.abspath(__file__))
        print("Directory initialized to: {p}. Note: This is the STARTING directory. {disclaimer}".format(
            p=self.pf.printf(self.pwd(False), "yellow", True, False), disclaimer=self.pf.printf("You can NOT go any further back.", "red", True, False)))
        self.addtolog("Directory initialized to:", self.pwd(False))
        self.origpath = self.pwd(False)
        return self.pwd(False)

    def cia(self, n=None):

        # Returns the current directory as an array.

        a = self.pwd(False).replace(chr(92), chr(47)).split(sep="/")
        for f in a:
            if f not in self.foldersvisited:
                self.foldersvisited.append(f)
        return a if n == None or n >= len(a) else a[-n]

    def pwd(self, px=True):

        # Prints the current directory.

        self.curpath = self.curpath.replace(chr(92), chr(47))
        if px:
            self.pf.printf("Current directory: {d}\n".format(
                d=self.curpath), "green", True, False)
        self.addtolog("Working directory printed:", self.curpath)
        os.chmod(self.curpath, 0o777)
        return self.curpath

    def mkdir(self, folder):

        # Creates a new directory.

        if not os.path.exists(folder):
            os.mkdir(folder)
            self.cd(folder)
            self.addtolog("Folder {f} added to:".format(
                f=folder), "Directory {px}".format(px=self.pwd(False)))

    def rmdir(self, folder):

        # Removes a directory if said directory is empty & exists, otherwise returns an error.

        try:
            if os.path.exists(folder):
                if os.path.isfile(folder):
                    os.remove(folder)
                    print("{tx} {fx} removed from folder {fi}".format(
                        tx="File", fx=folder, fi=self.pwd(False)))
                    self.addtolog("Item {fx} removed from folder:".format(
                        fx=folder), "{fi}".format(fi=self.pwd(False)))
                elif os.path.isdir(folder):
                    self.cd(folder)
                    for folderx in self.ls(f=True):
                        if len(self.ls(f=True)) == 0:
                            break
                        if os.path.isfile(folderx):
                            os.remove(folderx)
                            print("{tx} {fx} removed from folder {fi}".format(
                                tx="File", fx=folderx, fi=self.pwd(False)))
                            self.addtolog("Item {fx} removed from folder:".format(
                                fx=folderx), "{fi}".format(fi=self.pwd(False)))
                        elif os.path.isdir(folderx):
                            self.rmdir(folderx)
                            print("{tx} {fx} removed from folder {fi}".format(
                                tx="Folder", fx=folderx, fi=self.pwd(False)))
                            self.addtolog("Item {fx} removed from folder:".format(
                                fx=folderx), "{fi}".format(fi=self.pwd(False)))
                    self.cd("..")
                    os.rmdir(folder)
                    print("{tx} {fx} removed from folder {fi}".format(
                        tx="Folder", fx=folder, fi=self.pwd(False)))
                    self.addtolog("Item {fx} removed from folder:".format(
                        fx=folder), "{fi}".format(fi=self.pwd(False)))
            else:
                self.pf.perror("Folder {fx} does not exist in directory {dx}".format(
                    fx=folder, dx=self.pwd(False)))
        except OSError:
            self.pf.perror(
                "Folder {fx} could not be deleted, because it is not empty.".format(fx=folder))
            self.addtolog(
                "Folder {fx} could not be removed from directory:".format(fx=folder), "{dx}".format(dx=self.pwd(False)))
            self.command(note=7)

    def ls(self, f=False, adv="", n=None, lss=False, px=True):

        # Returns a list of folders in the current directory.

        folder = self.pwd() if len(adv) == 0 else adv
        ls = os.listdir(folder)
        lsn = []
        if not f:
            for folder in ls:
                if p.isdir(folder):
                    lsn.append(folder)
        returnable = (lsn if n == None or n >= len(
            lsn) else lsn[n]) if not lss else len(lsn)
        if px:
            println(returnable)
        self.addtolog("List of folders returned:", returnable)
        return returnable

    def cd(self, dirx):

        # Changes the current directory.

        oldpath = self.pwd(False)
        if p.exists(dirx):
            os.chdir(dirx)
            self.curpath = os.getcwd()
            if dirx == ".." or len(dirx) == 0:
                if self.deep == 0:
                    self.pf.perror(
                        "CANNOT GO BACK! You are at the beginning of the directory.")
                else:
                    self.deep -= 1
            else:
                a = dirx.replace(chr(92), chr(47)).split(sep="/")
                for f in a:
                    if f not in self.foldersvisited:
                        self.foldersvisited.append(f)
                self.deep += 1
            println("Directory changed to {d}".format(
                d=self.pwd(False)))
            self.addtolog("Directory has been changed from {o} to:".format(
                o=oldpath), self.pwd(False))
            return self.pwd(False)
        else:
            println("Directory could not be changed to {d} because the folder does not exist in the current directory {p}.".format(
                d=dirx, p=self.pf.perror(self.pwd())))
            self.addtolog("Directory could not be changed:", dirx)
            return -1

    def command(self, note=7, promptx=7, stop=6):

        # The command prompt.

        if note == 1:
            prompt = str(input(
                "Prompt: CHANGE DIRECTORY. Which folder from {l}? Type '..' if you want to go back.\n".format(l=self.ls(px=False))))
            self.cd(prompt)
            self.command(promptx)
        elif note == 2:
            self.ls()
            self.command(promptx)
        elif note == 3:
            self.pwd()
            self.command(promptx)
        elif note == 4:
            prompt = str(
                input("Prompt: MAKE DIRECTORY. What is the name of the folder?\t"))
            if len(prompt) > 0:
                self.mkdir(prompt)
            else:
                self.pf.perror("DID NOT SPECIFY A FOLDER!")
            self.command(promptx)
        elif note == 5:
            prompt = str(
                input("Prompt: REMOVE FOLDER. What is the name of the folder?\t"))
            if len(prompt) > 0:
                self.rmdir(prompt)
            else:
                self.pf.perror("DID NOT SPECIFY A FOLDER!")
            self.command(promptx)
        elif note == stop:
            self.pf.printf("Operations completed. To run again, please rerun the program.",
                           color="green", px=True)
            while not self.pwd(False) == self.origpath:
                if self.deep <= 0:
                    break
                self.cd("..")
            self.addtolog("STOP:", "Program has been stopped")
        elif note == promptx:
            prompt = str(input(
                "What would you like to do next? Type \033[1m CD \033[0m for CHANGE DIRECTORY, \033[1m LS \033[0m for FOLDER LIST, \033[1m PWD \033[0m for PRINT WORKING DIRECTORY, \033[1m MAKE \033[0m for MAKE DIRECTORY, \033[1m REMOVE \033[0m for REMOVE DIRECTORY or \033[1m STOP \033[0m to STOP.\t"))
            if "CD" in prompt.upper() or "CHANGE" in prompt.upper():
                self.command(1)
            elif "LS" in prompt.upper() or "LIST" in prompt.upper():
                self.command(2)
            elif "PWD" in prompt.upper() or "WORKING" in prompt.upper():
                self.command(3)
            elif "MAKE" in prompt.upper() or "MKDIR" in prompt.upper():
                self.command(4)
            elif "REMOVE" in prompt.upper() or "RMDIR" in prompt.upper():
                self.command(5)
            elif "STOP" in prompt.upper() or "QUIT" in prompt.upper():
                self.command(stop)
            else:
                self.pf.perror(
                    "YOU DID NOT TYPE ONE OF THE REQUIRED COMMANDS! TRY AGAIN!")
                self.command(promptx)


dirx = directory()
dirx.setpath()
dirx.command()
