import uuid

sessions = {}

def create_token(username: str):
    token = str(uuid.uuid4())
    sessions[token] = username
    return token

def verify_token(token: str):
    return sessions.get(token)
