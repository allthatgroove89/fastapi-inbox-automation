import os

def get_imap_config(email_user=None, email_pass=None, imap_server=None):
    if not email_user:
        email_user = os.getenv("EMAIL_USER")
    if not email_pass:
        email_pass = os.getenv("EMAIL_PASS")
    if not imap_server:
        imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")
    if not all([email_user, email_pass, imap_server]):
        raise ValueError("Missing IMAP credentials")
    return {
        "EMAIL_USER": email_user,
        "EMAIL_PASS": email_pass,
        "IMAP_SERVER": imap_server
    }
