from . import FileInterface


class Bss(FileInterface):

    def put(self, path: str, content: str):
        pass

    def get(self, path: str):
        pass

    def delete(self, path: str):
        arr = path.split('/')
        name = arr[-1]
        pass

    def url(self, path: str):
        pass
