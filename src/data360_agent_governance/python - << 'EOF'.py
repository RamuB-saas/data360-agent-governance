python - << 'EOF'
import os, time
import jwt
from dotenv import load_dotenv

load_dotenv(".env")
key = open(os.environ["SF_PRIVATE_KEY_PATH"]).read()
payload = {
    "iss": os.environ["3MVG9GCMQoQ6rpzSYLCxbmu3I1StdD54KvR03cUbwaLFfN307jUK_PyT90Pe56FLZn.OWM7c5NUpjAktcjV69"],
    "sub": os.environ["ram.dc360@lawar.com"],
    "aud": os.environ["https://osi-6b-dev-ed.develop.my.salesforce-setup.com/"],
    "exp": int(time.time()) + 300,
}
print(jwt.encode(payload, key, algorithm="RS256"))
EOF