def driver():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')

    print("Waiting for USB device...")

    for device in iter(monitor.poll, None):
        if 'ID_FS_TYPE' in device.properties:
            device_node = device.device_node  # e.g., /dev/sdb1
            mount_point = get_mount_point(device_node)

        if mount_point:
            return mount_point

def get_mount_point(device_node):
    for partition in psutil.disk_partitions():
        if device_node == partition.device:
            return partition.mountpoint
    return None


def open_file(file_path):
	print(file_path)
	subprocess.run(["xdg-open", file_path])  # Opens with default viewer
    

def get_recently_added_file(mount_path):
    try:
        # Command to find the recently added file
        cmd = f"find {mount_path} -type f -exec stat --format='%W %n' {{}} + | sort -nr | head -n1"
        
        # Execute the command
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                print("Recently added file:", output.split(' ', 1)[1])
                return output.split(' ', 1)[1]  # Return just the file path
            else:
                print("No files found.")
        else:
            print("Error:", result.stderr)
    
    except Exception as e:
        print("Exception occurred:", e)

def find_latest_file(directory):
    try:
        files = []
        
        # List all files in the directory
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                files.append(file)
        
        print(files)
        if not files:
            print("No files found in the directory.")
            return
        
        # Find the most recently accessed file
        latest_file = files[0]
        latest_time = os.path.getatime(os.path.join(directory, latest_file))
        
        for file in files[1:]:
            file_time = os.path.getatime(os.path.join(directory, file))
            print(latest_time,"           ",file_time)
            if file_time > latest_time:
                latest_file = file
                latest_time = file_time
        latest_file = os.path.join(directory, latest_file)
        return latest_file

    except Exception as e:
        print(f"Error: {e}")