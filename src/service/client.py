import base64
import pickle
from abc import ABC, abstractmethod

import cv2
import numpy as np
import zmq
from loguru import logger
from .. core.config import Settings
from . socket_server.models import ServerData


class AbstractSocketClient(ABC):
    @abstractmethod
    def show_stream_pc(self):
        pass

    @abstractmethod
    def parse_frame_from_server(self):
        pass

    @abstractmethod
    def get_server_response(self):
        pass

    @abstractmethod
    def parse_array_from_server(self):
        pass


class SocketClient(AbstractSocketClient):

    def __init__(self):
        self.settings = Settings()
        self.contex = zmq.Context()
        self.socket = self.contex.socket(zmq.SUB)
        self.socket.connect(self.settings.socket_server)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    @logger.catch
    def get_server_response(self):
        logger.info('Get data from socket')
        base64_server_data = self.socket.recv_string()
        logger.success('Data is received!')
        server_data = base64.b64decode(base64_server_data)
        server_data = pickle.loads(server_data)
        return server_data

    @logger.catch
    def parse_array_from_server(self):
        server_data: ServerData = self.get_server_response()
        return server_data.random_array

    @logger.catch
    def parse_frame_from_server(self):
        server_data = self.get_server_response()
        logger.success('Frame is received!')

        raw_image = base64.b64decode(server_data.frame)
        logger.success('Frame is decoded from base 64!')

        image = np.frombuffer(raw_image, dtype=np.uint8)
        logger.success('Frame is converted to numpy array!')

        frame = cv2.imdecode(image, 1)
        logger.success('Frame is decoded!')
        return frame

    def show_stream_pc(self):
        while True:
            try:
                frame = self.parse_frame_from_server()
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break


def show_stream_pc():
    client = SocketClient()
    client.show_stream_pc()
