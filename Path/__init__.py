from .Path import MyPath


class MyPathInterface:

    @staticmethod
    def myPathHome(path: list):
        MyPathVariable = MyPath(path, home=True)
        return str(MyPathVariable)

    @staticmethod
    def myPathCwd(path):
        MyPathVariable = MyPath(path, cwd=True)
        return str(MyPathVariable)

    @staticmethod
    def extendPath(path):
        pass

