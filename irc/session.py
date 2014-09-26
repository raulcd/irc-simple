import select
import socket

messages = {
        'password': 'PASS',
        'nickname': 'NICK',
        'username': 'USER',
        'join_channel': 'JOIN',
        }

class Session(object):

    _my_socket = None

    def __init__(self, *args, **kwargs):
        self._my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._my_socket.bind(('', 0))

    def connect(self, host, user, password, port=6667):
        host_port = (host, port)
        self._my_socket.connect(host_port)
        print(self._read_message())
        self._send_password_message(password)
        print(self._read_message())
        self._send_nick_message(user)
        print(self._read_message())
        self._send_user_message(user, host)
        print(self._read_message(timeout=60))
        print(self._read_message(timeout=60))

    def join(self, channel):
        self._send_join_channel_message(channel)

    def _generate_message(self, message_type, message):
        return bytes(" ".join([messages[message_type], message]), 'UTF-8')

    def _send_password_message(self, password):
        self._my_socket.send(self._generate_message('password', password))

    def _send_nick_message(self, nickname):
        self._my_socket.send(self._generate_message('nickname', nickname))

    def _send_user_message(self, user, host):
        my_intern_message = " ".join([user, '0 * :raulcd'])
        self._my_socket.send(self._generate_message('username', my_intern_message))

    def _read_message(self, timeout=5):
        ready = select.select([self._my_socket], [], [], timeout)
        if ready[0]:
            return self._my_socket.recv(1024)

    def _send_join_channel_message(self, channel):
        self._my_socket.send(self._generate_message('join_channel', channel))
        print(self._read_message())
        while True:
            self._read_message()
