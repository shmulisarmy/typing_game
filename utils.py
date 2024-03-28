import hashlib
from data import accountInfo

def getter(session, *attrs) -> list[any]:
    """
    funcType = (non decorator) wrapper
    takes in a session and attributes that a 
    user wants to get either from accountInfo or session
    """
    username = session.get("username")
    if username:
        return [accountInfo[username][attr] for attr in attrs]
    return [session.get(attr) for attr in attrs]

def setter(session, attr, value) -> None:
    """
    #! modifier
    funcType = (non decorator) wrapper
    takes in a session and one attribute that the
    user wants to set either into accountInfo or session
    """
    username = session.get("username")
    if username:
        accountInfo[username][attr] = value
    session[attr] = value


def secure(password: str) -> bool:
    return len(password) < 8


def hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(password_bytes)
    return hash_object.hexdigest()

