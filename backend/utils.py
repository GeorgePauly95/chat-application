import secrets


def is_empty(text):
    cleaned_text = text.strip()
    if cleaned_text == "":
        return True
    return False


def create_session_id():
    return secrets.token_urlsafe(32)
