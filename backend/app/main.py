import random
import string

from fastapi import FastAPI, Response, Header, status

app = FastAPI()

def generate_token():
  return "".join(random.choice(string.ascii_letters) for i in range(15))

PSEUDO_TOKEN = generate_token()

@app.get("/")
def read_root(response: Response, token: str = Header(None)):
  if token == PSEUDO_TOKEN:
    return {"result": "OK"}
  else:
    response.status_code = status.HTTP_403_FORBIDDEN
    return {"result": "NG"}

@app.get("/tokens")
def read_token():
  return PSEUDO_TOKEN

@app.get("/tokens/refresh")
def refresh_token():
  global PSEUDO_TOKEN
  PSEUDO_TOKEN = generate_token()
  return PSEUDO_TOKEN
