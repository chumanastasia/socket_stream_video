import base64
import random
import time
import pickle
from abc import ABC, abstractmethod


import cv2
import zmq
from pydantic import PositiveInt, validate_arguments
from loguru import logger
from art import tprint

from ... core.config import Settings
from . models import ServerData


class AbstractContentGenerator(ABC):
    @abstractmethod
    def get_camera_frames(self) -> bytes:
        pass

    @abstractmethod
    def get_random_array(self, size_array: PositiveInt = 10) -> tuple[int, ...]:
        pass


class AbstractSocketServer(ABC):
    @abstractmethod
    def run(self):
        pass


class ContentGenerator(AbstractContentGenerator):
    @logger.catch
    @validate_arguments
    def __init__(self, window_width: PositiveInt = 640, window_height: PositiveInt = 480) -> None:
        self.camera = cv2.VideoCapture(0)
        self.window_width = window_width
        self.window_height = window_height

    @logger.catch
    def get_camera_frames(self) -> bytes:
        frame = self.camera.read()[1]
        cv2.resize(frame, (self.window_width, self.window_height))
        buf = cv2.imencode('.jpg', frame)[1]
        return base64.b64encode(buf)

    @validate_arguments
    def get_random_array(self, size_array: PositiveInt = 10) -> tuple[int, ...]:
        return tuple(random.randint(0, 255) for _ in range(size_array))


class Server(AbstractSocketServer):
    def __init__(self):
        self.settings = Settings()
        self.content_generator = ContentGenerator()
        self.contex = zmq.Context()
        self.socket = self.contex.socket(zmq.PUB)
        self.socket.bind(self.settings.socket_server)

    def run(self):
        logger.info('Server is running')
        while True:
            try:
                random_array = self.content_generator.get_random_array()
                base64_frame = self.content_generator.get_camera_frames()

                logger.success(f'Random array is generated {random_array}.')
                logger.success('Frame is generated')

                server_data = ServerData(frame=base64_frame, random_array=random_array)

                socket_data = pickle.dumps(server_data)
                base64_socket_data = base64.b64encode(socket_data)

                self.socket.send(base64_socket_data)

                time.sleep(0.01)
                logger.success('Socket data is sent')

            except KeyboardInterrupt:
                self.socket.close()
                self.contex.term()

                tprint('Goodbye!', font='block')
                break


def run_socket_server():
    logger.info('Start socket server!')
    server = Server()
    server.run()
