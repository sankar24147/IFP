import os
import time

USB_PATH = "/home/sankar/usb_simulation"

def find_latest_file(directory):
    try:
        files = []
        
        # List all files in the directory
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                files.append(file)
        
        if not files:
            print("No files found in the directory.")
            return
        
        # Find the most recently accessed file
        latest_file = files[0]
        latest_time = os.path.getatime(os.path.join(directory, latest_file))
        
        for file in files[1:]:
            file_time = os.path.getatime(os.path.join(directory, file))
            if file_time > latest_time:
                latest_file = file
                latest_time = file_time
        
        print(f"Most recently accessed file: {latest_file}")

    except Exception as e:
        print(f"Error: {e}")


find_latest_file(USB_PATH)
