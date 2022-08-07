import signal
import sys
from threading import Thread

from art import tprint
from loguru import logger

from . app.flask_app import run_flask_server
from . service.socket_server.interface import run_socket_server


def signal_handler(signal_, frame) -> None:
    """
    Signal handler.
    :param signal_: signal
    :param frame: frame
    :return: None
    """
    signal_name = signal.Signals(signal_).name
    frame_name = frame.f_code.co_name
    logger.warning(f'Signal {signal_name} is received. Frame {frame_name}!')
    tprint('Goodbye!', font='block')
    sys.exit(0)


def main() -> None:
    """
    Main function.
    :return: None
    """
    socket_server_thread = Thread(target=run_socket_server, name='socket_server_thread')
    flask_server_thread = Thread(target=run_flask_server, name='flask_server_thread')
    # Запуск Сокет сервера
    socket_server_thread.start()
    # Запуск Flask сервера
    flask_server_thread.start()


if __name__ == '__main__':
    try:
        main()
        signal.signal(signal.SIGINT, signal_handler)
    except KeyboardInterrupt:
        tprint('Goodbye!', font='block')
    finally:
        sys.exit(0)
