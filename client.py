"""
Client for servers

Developer: Stanislav Alexandrovich Ermokhin

"""

import socket
from time import time


class ClientError(Exception):
    """ClientError class"""

    pass


class Client(object):
    """
    Socket creating connection embedded,
    this class has methods put and get - to send and get feedback on data
    and to receive data, respectively

    """

    def __init__(self, host, port, timeout=None):
        """
        Initialization method:
        host and port are for the server
        you wanna create connection with,
        timeout optional

        """

        self.host = host
        self.port = port
        self.timeout = timeout

    def get(self, name):
        """
        Method get allows you to receive data from the (host, port)
        and returns a dictionary of {metric: metric_value} if got
        any data on the 'name' back,
        otherwise - an empty dictionary.
        Raises ClientError in cases of:
        socket.error;
        (host, port) 'error' response.

        """

        try:
            with socket.create_connection((self.host, self.port)) as sock:
                sock.sendall(f'get {name}\n'.encode('utf8'))

                data = sock.recv(1024)
                msg = data.decode('utf8')
                if msg == 'ok\n\n':
                    return {}

                elif msg == 'error\nwrong command\n\n':
                    raise ClientError

                msg = msg[3:]
                msg = msg.split('\n')
                metrics = dict()

                for i in range(len(msg) - 2):
                    msg[i] = msg[i].split(' ')
                    metrics[msg[i][0]] = list()

                for i in range(len(msg) - 2):
                    lst = [int(msg[i][2]), float(msg[i][1])]
                    lst.extend(msg[i][3:])
                    metrics[msg[i][0]].append(tuple(lst))

                metrics = {key: sorted(metrics[key], key=lambda x: x[0])
                           for key in metrics}

                return metrics

        except socket.error:
            raise ClientError

    def put(self, key, value, timestamp=None):
        """
        Method put allows you to send data to (host, port)
        and receive feedback.
        Raises ClientError in cases of:
        socket.error;
        (host, port) 'error' response.

        """

        timestamp = timestamp or str(int(time()))

        try:

            with socket.create_connection((self.host, self.port)) as sock:
                msg = f'put {key} {value} {timestamp}\n'
                sock.sendall(msg.encode('utf8'))

                received = sock.recv(1024).decode('utf8')

                if received == 'error\nwrong command\n\n':
                    raise ClientError

        except socket.error:
            raise ClientError
