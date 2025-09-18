import imaplib
import email
from email.header import decode_header
import os

# Connect to an email server (e.g., Gmail)
def connect_to_email():
    email_user = "sankar12thboy@gmail.com"
    email_password = "msmctldctajvcejs"  # App password
    server = "imap.gmail.com"  # Gmail's IMAP server

    # Connect to the server and select the mailbox
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_user, email_password)
    mail.select("inbox")  # You can change to any folder

    return mail

# Fetch emails and download attachments
def fetch_attachments(mail, download_folder="/home/sankar/Desktop/IFP/simulation_lab/simulation/codes/Downloads"):
    # Search all emails
    status, messages = mail.search(None, "ALL")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    email_ids = messages[0].split()

    # Take only the last 10 emails
    latest_10 = email_ids[-5:]
    print(latest_10)

    for num in latest_10:
        status, msg_data = mail.fetch(num, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Get the subject and decode it
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')

                # Get the sender
                from_ = msg.get("From")

                print(f"Subject: {subject}")
                print(f"From: {from_}")

                # If the message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        filename = part.get_filename()
                        if filename:
                            filepath = os.path.join(download_folder, filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Downloaded: {filename}")