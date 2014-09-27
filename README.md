irc-simple
==========

Simple IRC client

The idea is to create a simple IRC client where you just need to connect:

```
import irc

session = irc.session(host='irc_host', user='username', password='password')
session.join('#channel_name', callback_function_on_message_received)
session.leave_channel('#channel_name')
session.close()
```
