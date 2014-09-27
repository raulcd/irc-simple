import irc

def test_connection():
    irc.session(host='irc.freenode.net', user='user', password='password')
    1 == 1

#def test_join_channel():
#    session = irc.session(host='sinisalo.freenode.net', user='user', password='password')
#    users = session.join('#python')
#    assert users is not None
