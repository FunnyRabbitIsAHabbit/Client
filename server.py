"""
Server for connection

Developer: Stanislav Alexandrovich Ermokhin

"""

import asyncio

dic = {}


class ClientServerProtocol(asyncio.Protocol):
    """A fine class"""

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        """A fine function"""

        self.transport = transport

    def data_received(self, data):
        """A finer function"""

        resp = process_requests(data.decode('utf8', 'ignore').split())
        self.transport.write(resp)


def process_requests(message):
    """

    :param message: decoded message
    :return: encoded response
    """

    if len(message):
        command = message[0]
        key_dict, values = message[1], message[2:]

        if command == 'put':
            if len(message) >= 3:
                if key_dict in dic:
                    if values not in dic[key_dict]:
                        dic[key_dict].append(values)

                else:
                    dic[key_dict] = list()
                    dic[key_dict].append(values)

                return 'ok\n\n'.encode('utf8')

            else:
                return 'error\nwrong command\n\n'.encode('utf8')

        elif command == 'get':
            try:
                key = message[1]

                if key == '*':
                    response = dic
                    response_str = 'ok\n'
                    for key_dict in response:
                        for i in range(len(response[key_dict])):
                            response_str += key_dict + ' ' + (' '.join(response[key_dict][i]))
                            response_str += '\n'

                    response_str += '\n'

                    return response_str.encode('utf8')

                elif key:
                    response = dic
                    response_str = 'ok\n'
                    key_dict = key
                    for i in range(len(response[key_dict])):
                        response_str += key_dict + ' ' + (' '.join(response[key_dict][i]))
                        response_str += '\n'

                    response_str += '\n'

                    return response_str.encode('utf8')

                else:
                    return 'error\nwrong command\n\n'.encode('utf8')

            except KeyError:
                return 'ok\n\n'.encode('utf8')

            except FileNotFoundError:
                return 'ok\n\n'.encode('utf8')

            except IndexError:
                return 'ok\n\n'.encode('utf8')

        else:
            return 'error\nwrong command\n\n'.encode('utf8')
    else:
        return 'error\nwrong command\n\n'.encode('utf8')


def run_server(host, port):
    """

    :param host: server host
    :param port: server port
    :return: None
    What it does is creating the connection on (host, port)
    as well as receiving data and sending response

    """

    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


run_server('127.0.0.1', 8888)
