import os
import subprocess
import json
from .collect_device import collect_devices

def get_usb_devices():
    usb_devices = []
    try:
        result = subprocess.check_output(
            "lsblk -o NAME,SIZE,MODEL,MOUNTPOINT,RM,TRAN -J",
            shell=True, text=True
        )
        data = json.loads(result)
        for device in data['blockdevices']:
            collect_devices(device, usb_devices)
    except Exception as e:
        print("Error getting USB devices:", e)
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
