from .session import Session

def session(**kwargs):
    session = Session()
    session.connect(**kwargs)
    return session

