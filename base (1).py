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
