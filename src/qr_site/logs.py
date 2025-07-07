import logging
import sys

__initd = False

def init():
    global __initd

    if __initd:
        return

    root_logger = logging.getLogger('qr_site')
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    __initd = True


def get_logger(name: str):
    if not name.startswith('qr_site.'):
        name = 'qr_site.' + name
    return logging.getLogger(name)