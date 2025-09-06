import os
import sys
import time
import subprocess

# For simple UP/DOWN key capture
try:
    import tty, termios
except ImportError:
    print("This script only works on Linux/Mac terminals.")
    sys.exit()

# --- SETTINGS ---
USB_PATH = "./../usb"  # Simulated USB folder

# --- FUNCTIONS ---

def list_files(path):
    try:
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except FileNotFoundError:
        print("USB folder not found!")
        return []

def get_key():
    """Capture single key press (non-blocking)"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)  # Read the next two chars for arrow keys
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def display_files(files, selected_idx):
    os.system('clear')  # Clear screen
    print("=== USB File Explorer ===\n")
    if not files:
        print("No files found.")
        return
    for idx, filename in enumerate(files):
        if idx == selected_idx:
            print(f"> {filename} <")
        else:
            print(f"  {filename}")

def open_file(file_path):
    print(f"\nOpening file: {file_path}")
    subprocess.run(["xdg-open", file_path])
    # Simulate opening (you can replace with actual open command)
    time.sleep(2)

# --- MAIN ---

def main():
    files = list_files(USB_PATH)
    selected_idx = 0

    while True:
        display_files(files, selected_idx)
        key = get_key()
        print(key)
        if key == '\x1b[A':  # UP arrow
            selected_idx = (selected_idx - 1) % len(files)
        elif key == '\x1b[B':  # DOWN arrow
            selected_idx = (selected_idx + 1) % len(files)
        elif key == '\n' or key=='\r':  # ENTER key
            file_to_open = os.path.join(USB_PATH, files[selected_idx])
            print("ENTER KEY WAS PRESSED")
            open_file(file_to_open)
        
        elif key.lower() == 'q':  # Quit
            print("\nExiting...")
            break
        

if __name__ == "__main__":
    main()
