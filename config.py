import os

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
KEYWORDS = os.environ.get('KEYWORDS', 'A36').split(',')
