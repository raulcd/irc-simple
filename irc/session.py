import asyncio
import logging

log = logging.getLogger(__name__)

messages = {
        'password': 'PASS',
        'nickname': 'NICK',
        'username': 'USER',
        'join_channel': 'JOIN',
        }

class IRCConnectionProtocol(asyncio.Protocol):

    def __init__(self, user, password):
        self._user = user
        self._password = password

    def connection_made(self, transport):
        transport.write(self._generate_message('password', self._password))
        transport.write(self._generate_message('nickname', self._user))
        my_intern_message = " ".join([self._user, '0 * :raulcd'])
        transport.write(self._generate_message('username', my_intern_message))

    def data_received(self, data):
        print('data received: {}'.format(data.decode()))

    def connection_lost(self, exc):
        print('server closed the connection')
        asyncio.get_event_loop().stop()

    def _generate_message(self, message_type, message):
        return bytes(" ".join([messages[message_type], message, "\n"]), 'UTF-8')

class Session(object):

    def __init__(self, host, user, password, **kwargs):
        irc_connection = IRCConnectionProtocol(user, password)
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(lambda: irc_connection, host, 6667)
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()
"""
        task = asyncio.Task(self._connect(host, user, password))
        task.add_done_callback(self._client_connected)
        loop.run_forever()
        self._connected = task.done()

    @asyncio.coroutine
    def _connect(self, host, user, password, port=6667):
        host_port = (host, port)
        client_reader, client_writer = yield from asyncio.open_connection(host, port)
        log.info("Connected to: {}:{}".format(host, port))
        task = asyncio.Task(self._read_message(client_reader))
        task.add_done_callback(self._read_message)
        task = asyncio.Task(self._send_user_data(client_writer, user, password))
        task.add_done_callback(self._client_connected)

    @asyncio.coroutine
    def _read_message(self, reader):
        data = yield from reader.readline()
        log.info("Received data: {}".format(data))
        return reader

    @asyncio.coroutine
    def _send_user_data(self, writer, user, password):
        writer.write(self._generate_message('password', password))
        writer.write(self._generate_message('nickname', user))
        my_intern_message = " ".join([user, '0 * :raulcd'])
        writer.write(self._generate_message('username', my_intern_message))

        
    def _client_connected(self, task):
        if task.exception():
            raise task.exception()
        self._connected = task.done() 

    def join(self, channel):
        self._send_join_channel_message(channel)

    def _send_join_channel_message(self, channel):
        self._my_socket.send(self._generate_message('join_channel', channel))
        print(self._read_message())
        while True:
            self._read_message()
"""
