import os

if os.getenv("RUNNING_IN_DOCKER") != "true":
    from dotenv import load_dotenv
    load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER")

def imap_config_present():
    return all([EMAIL_USER, EMAIL_PASS, IMAP_SERVER])
