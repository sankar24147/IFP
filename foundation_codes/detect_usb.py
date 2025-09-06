import os
import pyudev
import psutil

context = pyudev.Context()

def get_mount_point(device_node):
    for partition in psutil.disk_partitions():
        if device_node == partition.device:
            return partition.mountpoint
    return None

def get_usb_files(mount_point):
    try:
        return os.listdir(mount_point)
    except Exception as e:
        return [f"Error: {str(e)}"]

monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='block')

print("Waiting for USB device...")

for device in iter(monitor.poll, None):
    if 'ID_FS_TYPE' in device.properties:
        device_node = device.device_node  # e.g., /dev/sdb1
        mount_point = get_mount_point(device_node)

        if mount_point:
            print("USB Inserted:", mount_point)
            print("Files:", get_usb_files(mount_point))
        else:
            print(f"USB detected ({device_node}), but it's not mounted.")

