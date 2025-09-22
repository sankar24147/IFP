from flask import Flask,render_template,send_from_directory,request,send_file,redirect,url_for
from codes.latest_file import get_recently_added_file,open_file
from codes.display_devices import get_bluetooth_devices,get_usb_devices,get_wifi_devices
from codes.mail_projection import connect_to_email,fetch_attachments
from codes.instant_display import get_recently_added_file, open
from codes.voice_search import voice_search
import os, mimetypes, email, imaplib, subprocess, psutil, pyudev
from email.header import decode_header

app = Flask(__name__)

@app.route("/")
def home():
    usb_devices = get_usb_devices()
    
    return render_template(
        "home.html",
        usb_devices=usb_devices,
    )

@app.route("/display")
def displayFile():
    mount_path = "/home/sankar/Desktop/IFP/src_codes"
    latest_file = get_recently_added_file(mount_path)
    if latest_file:
        open_file(latest_file)
    else:
        return "No files found in the directory"

@app.route("/email")
def email_files():
    mail = connect_to_email()
    fetch_attachments(mail)
    mail.logout()

    folder_path = "/home/sankar/Desktop/IFP/simulation_lab/simulation/codes/Downloads"

    # Get all items in the folder
    all_items = os.listdir(folder_path)

    # Filter only files (ignore subfolders)
    files = [f for f in all_items if os.path.isfile(os.path.join(folder_path, f))]
    return render_template('mail_files.html',files=files)

@app.route("/downloads/<path:filename>")
def serve_download(filename):
    folder_path = "/home/sankar/Desktop/IFP/simulation_lab/simulation/codes/Downloads"
    return send_from_directory(folder_path, filename)

@app.route("/view_contents")
def list_files():
    path = request.args.get("path")

    if not path:
        return "Path is required", 400
    if not os.path.exists(path):
        return f"Path not found: {path}", 404
    if not os.path.isdir(path):
        return f"Not a directory: {path}", 400

    try:
        items = os.listdir(path)
    except Exception as e:
        return f"Error reading directory: {e}", 500

    folders = [i for i in items if os.path.isdir(os.path.join(path, i))]
    files = [i for i in items if os.path.isfile(os.path.join(path, i))]

    # calculate parent path (go up one level)
    parent_path = os.path.dirname(path) if path != "/" else None

    return render_template("view_contents.html", path=path, folders=folders, files=files, parent_path=parent_path)

@app.route("/instant_display")
def instant_display():
    mount_path = request.args.get("path")
    file_path = get_recently_added_file(mount_path)
    if not file_path:
        return "No file specified", 400
    open(file_path)
    # Redirect back to the devices page after triggering display
    return redirect(url_for("home"))  # replace with your main route


@app.route("/open")
def open_file():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return "File not found", 404
    if not os.path.isfile(path):
        return "Not a file", 400

    # Try to guess the MIME type
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "application/octet-stream"  # fallback

    return send_file(path, mimetype=mime_type, as_attachment=False)

@app.route("/project")
def project():
    file_path = request.args.get("file")
    if not file_path or not os.path.exists(file_path):
        return "File not found", 404
    return send_file(file_path)

@app.route("/voice_search")
def voice_search_route():
    response = voice_search()
    return response




if __name__ == "__main__":
    app.run(debug=True)