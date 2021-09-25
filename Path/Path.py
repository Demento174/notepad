from pathlib import Path


class MyPath:
    path = None
    home = None
    cwd = None
    mainFolder = None

    def __init__(self, path: list, home=False, cwd=False, mainFolder=False):
        self.path = path

        if ((home==True and cwd==True) or (home==False and cwd == False)) and (mainFolder == False):
            raise 'Выберите стартовую директорию'
        elif home== True:

            self.__set_home()
            self.mainFolder = self.home
        elif cwd== True:
            self.__set_cwd()
            self.mainFolder = self.cwd
        elif mainFolder is not False:
            self.mainFolder = mainFolder

    def __set_home(self):
        self.home = Path.home()

    def __set_cwd(self):
        self.cwd = Path.cwd()

    def add_path(self,listPath:list):
        self.path.extend(listPath)

    def __str__(self):
        return str(Path(self.mainFolder, *self.path))



