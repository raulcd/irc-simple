from .session import Session

def session(**kwargs):
    session = Session(**kwargs)
    return session

