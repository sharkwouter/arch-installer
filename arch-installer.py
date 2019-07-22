#!/usr/bin/env python3
from partitioner import Partitioner
from mount import Mount

partitioner = Partitioner()

# Let the user choose the disk to install to
choice_made = False
rootfs_partition = None
while not choice_made:
    partitioner.print_devices()
    choice = input("Choose a device by path: ")
    for device in partitioner.get_devices():
        if device.path == choice:
            choice_made = True
            rootfs_partition = partitioner.repartition(device)
            break
    if not choice_made:
        print("{} is not a valid device!".format(choice))

rootfs_mount = Mount(rootfs_partition.path, "/mnt")