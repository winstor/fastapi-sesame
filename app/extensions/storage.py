from .file_system import FileInterface
from app.config import filesystems
from .file_system import Bss, Local


class Storage:
    __config: dict = {}
    __obj: FileInterface = None

    def __int__(self):
        self.__config = filesystems.disks.get(filesystems.default)

    def disk(self, name: str = None):
        self.__config = filesystems.disks.get(name)
        return self.__get_obj()

    def __get_obj(self) -> FileInterface:
        driver = self.__config.get('driver')
        return driver(self.__config)

    def put(self, path: str, content: str):
        return self.__get_obj().put(path, content)

    def get(self, path: str):
        return self.__get_obj().get(path)

    def delete(self, path: str):
        return self.__get_obj().delete(path)

    def url(self, path: str):
        return self.__get_obj().url(path)


storage = Storage()

