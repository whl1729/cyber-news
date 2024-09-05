import socket

import socks


def init():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7078)
    socket.socket = socks.socksocket
