import os
import subprocess
import json

def collect_devices(device, usb_devices):
    """
    Collect only parent USB devices (not partitions).
    """
    tran = device.get('tran')
    rm = device.get('rm')

    # Sysfs check for USB
    sys_path = f"/sys/block/{device['name'].replace('/','')}/device"
    is_usb = False
    if os.path.exists(sys_path):
        try:
            if 'usb' in os.readlink(sys_path).lower():
                is_usb = True
        except Exception:
            pass

    # Only add the *main device* (skip partitions/children)
    if (rm is True or tran == 'usb' or is_usb):
        mountpoint = device.get('mountpoint')
        # If parent has no mountpoint, check children
        if not mountpoint and 'children' in device:
            for child in device['children']:
                if child.get('mountpoint'):
                    mountpoint = child['mountpoint']
                    break

        usb_devices.append({
            'model': device.get('model', 'Unknown'),
            'size': device['size'],
            'mountpoint': mountpoint or 'Not Mounted'
        })