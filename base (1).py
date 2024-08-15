import pickle
import re
import copy

class File:

    def __init__(self ,address) -> None:
        self.__name = address[-1]
        self.__address = address
        self.__content = ""

    
    def set_address(self ,address):
        self.__address = address

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address


    def show(self):
        print(self.__content)

    def write(self ,text):
        self.__content += text


class Folder:
    
    def __init__(self ,address) -> None:
        self.__name = address[-1]
        self.__address = address
        self.__folder = []


    def search(self ,name):
        for file in self.__folder:
            if file.get_name() == name:
                return file
        return False

    def add(self ,file:File):
        self.__folder.append(file)
        file.set_address(self.get_address() + f"/{file.get_name()}")  

    def show(self):
        for indx , val in enumerate(self.__folder):
            print(f"{indx+1}) {val.get_name()} : {type(val)}")
        
    def remove(self ,name):
        for inx , val in  enumerate(self.__folder):
            if val.get_name() == name:
                self.__folder.pop(inx)

    def set_address(self ,address):
        self.__address = address

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address



class Windows:

    current_address = ["root"]


    def regex(self ,address):
        if re.search("^(/[^/ ]*)+/?$" ,address) != None:
            self.path_type = "abs"
        if re.search("^(?!-)[a-z0-9-]+(?<!-)(/(?!-)[a-z0-9-]+(?<!-))*(/(?!-\.)[a-z0-9-\.]+(?<!-\.))?$" ,address) != None:
            self.path_type = "rel"
        return False
    

    def save(self):
        with open('win_data.pkl', 'wb') as otp:
            pickle.dump(self.root , otp)


    def load(self):
        try:
            with open('win_data.pkl', 'rb') as inp:
                data = pickle.load(inp)
            self.root = data
        except:
            self.root = Folder("/root")


    def start(self):
        while True:
            command = input("enter your command\n")
            if command == "save":
                self.save()
                break
            command = command.split(" ")
            if len(command) == 3:
                self.regex(command[2]) 
                name = command[1]
                com = command[0]
            else:
                com = command[0]    
                self.regex(command[1])

            if self.path_type == "abs":
                address = command[1][1:].split("/")
            elif self.path_type == "rel":
                address = self.current_address + command[1].split("/")
            else:
                print("wrong address")
            

            
            if com == "pwd":
                self.pwd(address)

            elif com == "mkdir":
                self.mkdir(address)

            elif com == "mkfil":
                self.mkfil(address)

            elif com == "cp":
                self.cp(name ,address)

            elif com == "cat":
                self.cat(address)
            
            elif com == "mv":
                self.mv(name ,address)
            
            elif com == "find":
                self.find(address)

            elif com == "rm":
                self.rm(address)

            elif com == "cd":
                self.cd(address)

            else:
                print("wrong input")
                


    
    def search(self ,address):
        if len(address) == 1:
            return self.root
        prv = self.root.search(address[1])
        for i in range(2,len(address)):
            prv = prv.search(address[i])
        return prv

        

    def pwd(self ,address):
        self.search(address).show()

    def mkdir(self ,address):
        paret_path = address[:-1]
        self.search(paret_path).add(Folder(address))
        

    def mkfil(self ,address):
        paret_path = address[:-1]
        self.search(paret_path).add(File(address))

    def cp(self ,name ,paste_address):
        file = self.search(self.current_address.append(name))
        copy_file = copy.deepcopy(file)
        copy_file.set_address(paste_address.append(name))
        self.search(paste_address).add(copy_file)


    def cat(self ,address):
        file = self.search(address)
        if type(file) == File:
            file.show()
        else:
            print("cat command is not defined for directories")

    def mv(self ,name ,paste_address):
        file = self.search(self.current_address.append(name))
        self.search(self.current_address).remove(name)
        file.set_address(paste_address.append(name))
        self.search(paste_address).add(file)

    def find(self ,address):
        self.search(address)

    def rm(self ,address):
        self.search(address[:-1]).remove(address[-1])

    def cd(self ,address):
        self.current_address = address
        print(f"active directory : {self.current_address}")



win = Windows()
win.load()
win.start()