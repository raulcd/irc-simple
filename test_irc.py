import irc

def test_connection():
    irc.session(host='irc.freenode.net', user='telo', password='password')

def test_join_channel():
    session = irc.session(host='sinisalo.freenode.net', user='xxxir', password='password')
    session.join('#python')
