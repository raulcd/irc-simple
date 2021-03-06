try:
    import asyncio
except ImportError:
    import trollius as asyncio


messages = {'password': 'PASS',
            'nickname': 'NICK',
            'username': 'USER',
            'join_channel': 'JOIN',
            'away': 'AWAY',
            'list': 'LIST',
            'pong': 'PONG',
            'message': 'PRIVMSG',
            }


class IRCConnectionProtocol(asyncio.Protocol):

    def __init__(self, user, password):
        self._user = user
        self._password = password
        self.channel_callbacks = {}

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self._generate_message('password', self._password))
        asyncio.wait(transport.write(
                     self._generate_message('nickname', self._user)))
        my_intern_message = " ".join([self._user, '0 * :purple'])
        asyncio.wait(transport.write(
                     self._generate_message('username', my_intern_message)))

    def data_received(self, data):
        message_received = data.decode()
        print('data received: {}'.format(message_received))
        if message_received.count('PING'):
            self.transport.write(self._generate_message('pong', ''))
        elif message_received.count('PRIVMSG'):
            callback_functions = [callback
                                  for channel, callback
                                  in self.channel_callbacks.items()
                                  if message_received.count(channel)]
            for callback in callback_functions:
                callback(data)

    def connection_lost(self, exc):
        print('server closed the connection')
        asyncio.get_event_loop().stop()

    @asyncio.coroutine
    def join_channel(self, channel, on_message_received):
        self.transport.write(self._generate_message('join_channel', channel))
        self.channel_callbacks[channel] = on_message_received

    def _generate_message(self, message_type, message):
        return " ".join([messages[message_type],
                         message, "\n"]).encode('UTF-8')


class Session(object):

    def __init__(self, host, user, password, **kwargs):
        self.irc_connection = IRCConnectionProtocol(user, password)
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(lambda: self.irc_connection, host, 6667)
        loop.run_until_complete(coro)

    def join(self, channel, on_message_received):
        coro = self.irc_connection.join_channel(channel, on_message_received)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(coro)

    def run_forever(self):
        loop = asyncio.get_event_loop()
        loop.run_forever()

    def close(self):
        loop = asyncio.get_event_loop()
        loop.close()
