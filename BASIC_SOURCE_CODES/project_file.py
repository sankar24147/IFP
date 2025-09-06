import os
import subprocess

def open_file(file_path):
    subprocess.run(["xdg-open", file_path])  # Opens with default viewer


latest_file='/home/sankar/Desktop/IFP SMART PROJECTOR/sp_10th_mar'

if latest_file:
    open_file(latest_file)
