from datetime import datetime, timedelta
import jwt
import os

# Create a secret key constant variable
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

def encode_token(customer_id):
    payload = {
        'exp': datetime.now() + timedelta(hours=1),
        'iat': datetime.now(),
        'sub': customer_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


print(encode_token(1))

# iat = issued at