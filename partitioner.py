import string
import parted
import subprocess


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class Partitioner:

    def __init__(self):
        self.__devices = parted.getAllDevices()

    def refresh_devices(self):
        self.__devices = parted.getAllDevices()

    def get_devices(self):
        return self.__devices

    def print_devices(self) -> None:
        self.refresh_devices()
        for device in self.__devices:
            self.print_device(device)

    def print_device(self, device: parted.Device):
        print(color.BOLD + "Disk {}".format(device.model) + color.END)
        print("Size: {}".format(self.bytes_to_readable(device.sectorSize * device.length)))
        print("Path: {}".format(device.path))

        # Print partitions
        disk = parted.newDisk(device)
        print(color.BOLD + "Partition\t\tSize\t\tFile System" + color.END)
        for partition in disk.getPrimaryPartitions():
            path = partition.path
            size = self.bytes_to_readable(partition.geometry.length*device.sectorSize)
            type = partition.fileSystem.type
            print("{}\t\t{}\t\t{}".format(path, size, type))
        print("")

    def repartition(self, device: parted.Device) -> bool:
        disk = parted.newDisk(device)
        # Delete the current partitions and create a new one
        if disk.deleteAllPartitions() and disk.commit():
            new_partition = self.create_partition(device, 0, device.getLength()-1)
            if not new_partition:
                return False

            # Format the newly created partition and whether or not the return code was 0
            result = subprocess.run(["/usr/sbin/mkfs", "-F", "-t", "ext4", "{}".format(new_partition.path)])
            return result.returncode == 0
        return False

    def get_partitions_device(self, device: parted.Device):
        disk = parted.newDisk(device)
        return disk.getPrimaryPartitions()

    def format_partition(self, partition: parted.Partition):
        disk = partition.disk()

    def create_partition(self, device: parted.Device, start: int, length: int=None, end: int=None, partition_type: int=parted.PARTITION_NORMAL, filesystem_type: string="ext4",) -> parted.Partition:
        disk = parted.newDisk(device)
        geometry = parted.Geometry(device=device, start=start, end=end, length=length)
        filesystem = parted.FileSystem(type=filesystem_type, geometry=geometry)
        constraint = parted.Constraint(device=device)

        partition = parted.Partition(disk, partition_type, geometry=geometry, fs=filesystem)

        # Create the partition
        if not disk.addPartition(partition, constraint):
            return None
        if not disk.commit():
            return None

        return partition

    def bytes_to_readable(self, size: int) -> string:
        if size >= (1024**4):
            return "{} TB".format(round(size / 1024**4, 1))
        elif size >= (1024**3):
            return "{} GB".format(round(size / 1024**3, 1))
        elif size >= (1024**2):
            return "{} MB".format(round(size / 1024**2, 1))
        elif size >= (1024**1):
            return "{} KB".format(round(size / 1024, 1))
        else:
            return "{} bytes".format(size)
