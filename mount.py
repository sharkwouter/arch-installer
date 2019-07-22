import parted
import subprocess
import string


class Mount:

    def __init__(self, path: string, destination: string):
        self.__path = path
        self.__destination = destination
        self.__mount(self.__path, self.__destination)

    def __mount(self, path, destination):
        result = subprocess.run(["/usr/bin/mount", path, destination])
        if result.returncode != 0:
            raise Exception("The partition {} could not be mounted at {}".format(path, destination))

    def __str__(self):
        return self.__destination

    def get_device_path(self):
        return self.__path

    def unmount(self):
        result = subprocess.run(["/usr/bin/umount", self.__destination])
        return result.returncode == 0
