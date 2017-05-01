import multiprocessing
import os
import socket
import time

import pytest

from app import create_app
from app.models import db


def get_open_port():
    """ Find free port on a local system """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def wait_until(predicate, timeout=5, interval=0.05, *args, **kwargs):
    """ Helper to wait for some conditions with periodic polling.

    Based on http://stackoverflow.com/a/2785908/186912
    by Alex Martelli

    :param predicate: function to check conditions
    :param timeout: total wait timeout to break
    :param interval: interval between polls
    :param args: predicate args
    :param kwargs: predicate kwargs
    :return:
    """
    mustend = time.time() + timeout
    while time.time() < mustend:
        if predicate(*args, **kwargs):
            return True
        time.sleep(interval)
    return False


@pytest.fixture
def server():
    app = create_app()

    port = get_open_port()
    app.url = 'http://localhost:{}'.format(port)

    def start():
        print("start server")
        app.run(port=port)

    p = multiprocessing.Process(target=start)
    p.start()

    def check():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('localhost', port))
            return True
        except Exception:
            return False
        finally:
            s.close()

    rc = wait_until(check)
    assert rc, "failed to start service"

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    p.terminate()
