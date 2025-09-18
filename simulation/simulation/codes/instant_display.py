import subprocess
import os   

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


def open(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".ppt", ".pptx", ".odp"]:
        # Use LibreOffice for presentations
        subprocess.Popen(["libreoffice", "--show", file_path])
    else:
        # Serve via Flask and open in browser
        url = f"http://localhost:5000/project?file={file_path}"
        #subprocess.Popen(["firefox", "--start-fullscreen", url])
        subprocess.Popen(["firefox", "--kiosk", url])
        # or use "google-chrome" / "firefox" depending on your system
