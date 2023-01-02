from Crypto.PublicKey import RSA
import random
import string
import datetime


def generate_rsa_key():
    """Generate priv,pub key pair for test"""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def get_random_string(length):
    """Generate random string of given length"""
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

EXAMPLE_PRIVATE_KEY, EXAMPLE_PUBLIC_KEY = generate_rsa_key()

TIMESTAMP_FORMAT = '%Y-%m-%d'
EXAMPLE_USER_REQUEST = {
    'email': 'jdoe',
    'password': 'pwd',
    'registereddate': '2000-01-01',
    'timezone': 'GMT+1',
}
EXAMPLE_USER = {
    'userid': '123',
    'username': 'jdoe',
    'passhash': b'hjfsrf#jrsfj',
    'registereddate': datetime.strptime('2000-01-01', TIMESTAMP_FORMAT).date(),
    'timezone': 'GMT+1',
}
EXPECTED_FIELDS = [
    'username',
    'password',
    'registereddate',
    'timezone',
]

# Usernames must be >1 and <=15 chars, alphanumeric and underscores
INVALID_USERNAMES = [
    None, # null
    "", # empty string
    " ", # only space
    "b", # single character
    " user", # starting with space
    "*$&%($", # non alphanumeric characters
    "user*new", # alphanumeric with non alphanumeric characters
    "🏦💸", # emojis
    "user1💸", # alphanumeric with emojis
    get_random_string(16), # 16 characters
    " {}".format(get_random_string(15)), # 15 characters + leading space
    "{} ".format(get_random_string(15)), # 15 characters + trailing space
    "{}".format(get_random_string(100)), # 100 characters
    ]