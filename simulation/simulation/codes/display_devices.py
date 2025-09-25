import os
import subprocess
import json
from .collect_device import collect_devices

def get_usb_devices():
    # usb_devices = []
    # try:
    #     result = subprocess.check_output(
    #         "lsblk -o NAME,SIZE,MODEL,MOUNTPOINT,RM,TRAN -J",
    #         shell=True, text=True
    #     )
    #     data = json.loads(result)
    #     for device in data['blockdevices']:
    #         collect_devices(device, usb_devices)
    # except Exception as e:
    #     print("Error getting USB devices:", e)
    # return usb_devices

    '''
    usb_devices = []

    # Detect block devices (pendrives, external HDDs)
    try:
        result = subprocess.check_output(
            "lsblk -o NAME,SIZE,MODEL,MOUNTPOINT,RM,TRAN -J",
            shell=True, text=True
        )
        data = json.loads(result)
        for device in data['blockdevices']:
            collect_devices(device, usb_devices)
    except Exception as e:
        print("Error getting USB block devices:", e)

    # Detect MTP devices (phones)
    gvfs_path = "/run/user/{}/gvfs".format(os.getuid())
    if os.path.exists(gvfs_path):
        for entry in os.listdir(gvfs_path):
            if entry.startswith("mtp:"):
                mountpoint = os.path.join(gvfs_path, entry)
                device_name = "MTP Device"  # Default name
                print(mountpoint,"    AAAAAAAAAAAAAAAAAAAAAAAAA")

                # Use gvfs-info to get the real name
                try:
                    info_result = subprocess.check_output(
                        f"gvfs-info '{mountpoint}'",
                        shell=True, text=True
                    )
                    for line in info_result.splitlines():
                        if "standard::name:" in line:
                            device_name = line.split("standard::name:")[1].strip()
                            break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print(f"Could not get info for {mountpoint}, using default name.")
                
                usb_devices.append({
                    "model": device_name,
                    "mountpoint": mountpoint,
                    "type": "MTP"
                })

    return usb_devices
    '''
    usb_devices = []

    # Detect block devices (pendrives, external HDDs)
    try:
        result = subprocess.check_output(
            "lsblk -o NAME,SIZE,MODEL,MOUNTPOINT,RM,TRAN -J",
            shell=True, text=True
        )
        data = json.loads(result)
        for device in data['blockdevices']:
            collect_devices(device, usb_devices)
    except Exception as e:
        print("Error getting USB block devices:", e)

    # Detect MTP devices (phones) by parsing gvfs entry
    gvfs_path = f"/run/user/{os.getuid()}/gvfs"
    if os.path.exists(gvfs_path):
        for entry in os.listdir(gvfs_path):
            if entry.startswith("mtp:"):
                raw_name = entry.replace("mtp:host=", "")
                parts = raw_name.split("_")
                if len(parts) >= 2:
                    phone_name = f"{parts[0]} {parts[1]}"   # e.g. INFINIX Infinix
                else:
                    phone_name = raw_name

                usb_devices.append({
                    "model": phone_name,
                    "size": "Unknown (MTP)",
                    "mountpoint": os.path.join(gvfs_path, entry),
                    "type": "MTP"
                })

    return usb_devices

def get_wifi_devices():
    wifi_devices = []
    try:
        result = subprocess.check_output("nmcli -t -f SSID,DEVICE dev wifi", shell=True, text=True)
        lines = result.strip().split("\n")
        for line in lines:
            if line:
                ssid, device = line.split(":")
                wifi_devices.append({'ssid': ssid, 'interface': device})
    except Exception as e:
        print("Error getting Wi-Fi devices:", e)
    return wifi_devices

def get_bluetooth_devices():
    bt_devices = []
    try:
        result = subprocess.check_output("bluetoothctl devices", shell=True, text=True)
        lines = result.strip().split("\n")
        for line in lines:
            parts = line.split(" ", 2)
            if len(parts) == 3:
                bt_devices.append({'mac': parts[1], 'name': parts[2]})
    except Exception as e:
        print("Error getting Bluetooth devices:", e)
    return bt_devices

if __name__ == "__main__":
    print("USB Storage Devices:")
    for d in get_usb_devices():
        print(f"{d['name']} - {d['model']} - {d['size']} - {d['mountpoint']}")
    
    print("\nWi-Fi Devices (Nearby Networks):")
    for d in get_wifi_devices():
        print(f"{d['ssid']} - Interface: {d['interface']}")
    
    print("\nBluetooth Devices:")
    for d in get_bluetooth_devices():
        print(f"{d['name']} - MAC: {d['mac']}")
