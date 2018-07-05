import uuid
import hashlib


def hash_password_with_salt(text, salt):
    """
        Basic hashing function for a text using random unique salt.
    """
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt


def matchHashedText(hashedText, providedText):
    """
        Check for the text in the hashed text
    """
    _hashedText, salt = hashedText.split(':')
    return _hashedText == hashlib.sha256(salt.encode() + providedText.encode()).hexdigest()


def get_random_uuid():
    """
    Creates and Returns a random salt
    """
    return uuid.uuid4().hex


def create_token(key, text, expiration_time):
    from config import COOKIE_DELIMITER
    return hashlib.sha256(
        text.encode() + key.encode()).hexdigest() + COOKIE_DELIMITER + text + COOKIE_DELIMITER + expiration_time


def is_token_signature_validated(auth_token, key):
    try:
        from config import COOKIE_DELIMITER
        hash_value, text, expiration_date = auth_token.split(COOKIE_DELIMITER)
        return (
            auth_token == create_token(key,
                                       text,
                                       expiration_date
                                       ))

    except AttributeError:
        return False
