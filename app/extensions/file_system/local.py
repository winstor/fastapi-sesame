from . import FileInterface


class Local(FileInterface):

    def put(self, path: str, content: str):
        pass

    def get(self, path: str):
        pass

    def delete(self, path: str):
        pass

    def url(self, path: str):
        pass

