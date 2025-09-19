import imaplib
from email import message_from_bytes
from backend.imap_config import IMAP_SERVER
from backend.entities.user import User

class Creds:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

def get_email_credentials(user: User) -> Creds:
    return Creds(email=user.email, password=user.email_password)

def get_imap_config(email: str, password: str) -> dict:
    return {
        "server": IMAP_SERVER,
        "email": email,
        "password": password
    }

def sync_emails(imap_config: dict, folder: str = '"INBOX"') -> list:
    server = imap_config["server"]
    email = imap_config["email"]
    password = imap_config["password"]

    def _print_folders(imap):
        status, folders = imap.list()
        print("Available folders:")
        for f in folders:
            print(f.decode())

    def _print_selected(folder, messages):
        print(f"Selected folder: {folder}")
        print(f"Message count: {len(messages[0].split())}")

    def _sync(debug=False):
        imap = imaplib.IMAP4_SSL(server)
        imap.login(email, password)
        if debug:
            _print_folders(imap)
        imap.select(folder)
        status, messages = imap.search(None, "ALL")
        if debug:
            _print_selected(folder, messages)
        email_list = []
        for num in messages[0].split():
            status, data = imap.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = message_from_bytes(raw_email)
            subject = msg["subject"]
            body = msg.get_payload(decode=True)
            if isinstance(body, bytes):
                body = body.decode(errors="ignore")
            email_list.append({
                "id": num.decode(),
                "subject": subject,
                "body": body,
                "folder": folder
            })
        imap.logout()
        return email_list

    # Accept debug as kwarg for backward compatibility
    import inspect
    frame = inspect.currentframe().f_back
    debug = frame.f_locals.get('debug', False)
    return _sync(debug=debug)

def fetch_emails_for(user: User, folder: str = '"INBOX"') -> list:
    creds = get_email_credentials(user)
    imap_config = get_imap_config(creds.email, creds.password)
    return sync_emails(imap_config, folder)
