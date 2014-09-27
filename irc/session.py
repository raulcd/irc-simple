import asyncio
import logging

log = logging.getLogger(__name__)

messages = {
        'password': 'PASS',
        'nickname': 'NICK',
        'username': 'USER',
        'join_channel': 'JOIN',
        'away': 'AWAY',
        'list': 'LIST',
        'pong': 'PONG',
        }

class IRCConnectionProtocol(asyncio.Protocol):

    def __init__(self, user, password):
        self._user = user
        self._password = password

    def connection_made(self, transport):
        transport.write(self._generate_message('password', self._password))
        asyncio.wait(transport.write(self._generate_message('nickname', self._user)))
        my_intern_message = " ".join([self._user, '0 * :raulcd'])
        asyncio.wait(transport.write(self._generate_message('username', my_intern_message)))
        self.transport = transport

    def data_received(self, data):
        message_received = data.decode()
        print('data received: {}'.format(message_received))
        if message_received.count('PING'):
            self.transport.write(self._generate_message('pong', ''))


    def connection_lost(self, exc):
        print('server closed the connection')
        asyncio.get_event_loop().stop()

    @asyncio.coroutine
    def join_channel(self, channel):
        self.transport.write(self._generate_message('join_channel', channel))

    def _generate_message(self, message_type, message):
        return bytes(" ".join([messages[message_type], message, "\n"]), 'UTF-8')

class Session(object):

    def __init__(self, host, user, password, **kwargs):
        self.irc_connection = IRCConnectionProtocol(user, password)
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(lambda: self.irc_connection, host, 6667)
        loop.run_until_complete(coro)
        
    def join(self, channel):
        coro = self.irc_connection.join_channel(channel)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(coro)
        loop.run_forever()

    def close(self):
        loop = asyncio.get_event_loop()
        loop.close()

