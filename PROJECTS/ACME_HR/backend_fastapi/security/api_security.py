import json
from datetime import timezone, datetime, timedelta

import bcrypt
import jwt
import base64

# this is to hash the password, so that we dont store plain passwords in db
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed_password.encode())

signin_secret_key = "only-server-knows-this-key-1234567"
exp_minutes = 30


# This function is to geneate JWT bearer token: which needs claims, header, signature
def create_access_token(employee_code: str, role: str) -> str:
    now = datetime.now(timezone.utc)

    claims = {
      "sub": employee_code,
      "iat": now,
      "exp": now + timedelta(minutes=exp_minutes),
      "role": role,
    }

    return jwt.encode(claims, signin_secret_key, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, signin_secret_key, algorithms=["HS256"])


if __name__ == "__main__":
    # create and decode access token
    access_token = create_access_token("E-1234", role="admin")
    print(access_token)

    header, payload, signature = access_token.split(".")

    fake_payload = json.dumps({'sub': 'E-1234', 'iat': 1794373544, 'exp': 1794375344, 'role': 'CEO'})
    fake_claims = base64.urlsafe_b64encode(fake_payload.encode()).decode().rstrip("=")
    print("fake_claims", fake_claims)

    fake_access_token = header + "." + fake_claims + "." + signature
    print("fake_access_token", fake_access_token)
    token_claims = decode_access_token(access_token)
    print(token_claims)


    decode_access_token(fake_access_token)





