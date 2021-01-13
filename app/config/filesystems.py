from app.extensions.file_system import Bss, Local

default = 'bss'

disks = {
    "local": {
        "driver": Local,
        "root": "/"
    },
    "bss": {
        "driver": Bss,
        "key": "145454",
        "secret": "asdjassf",
        "url": "http://127.0.0.1:8000/",
    }
}
