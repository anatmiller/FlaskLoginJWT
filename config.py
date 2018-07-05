from hashing import hash_password_with_salt

PORT_NUMBER = 4443
EMAIL, PASSWORD = (0, 1)
AUTH_MAX_DAYS = 30
SESSION_MAX_MINUTES = 1
DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
COOKIE_SIGNATURE_POSITION = 0
COOKIE_ID_POSITION = 1
COOKIE_EXPIRATION_DATE_POSITION = 2
COOKIE_DELIMITER = '|'
# to generate new keys : base64.b64encode(os.urandom(64)).decode('utf-8')
AUTH_KEY = 'SMPw/1eaWkodz2SFHiyjJTvYRu5rjHPkEPubxauCPJKzIHZY6nX+/moni0W9q76kzbsrBtf7NhRtJI69HzKY+A=='
SESSION_KEY = '/Zh4X0X3kI5EXRtEagLhGrlETue5ieNDzHXpcX55N8srqpjIgIL+EFMgDYT1jCLVDkHAh9amueOjNq3j3rdGLA=='

users = [
         ('yaniv@mega-sec.com', hash_password_with_salt('yaniv1234', '555')),
         ('yossi@mega-sec.com', hash_password_with_salt('yossi1234', '333')),
         ('john-doe@mega-sec.com', hash_password_with_salt('john1234', '222'))
        ]