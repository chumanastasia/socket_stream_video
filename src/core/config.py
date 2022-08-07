from pydantic import BaseSettings, AnyUrl, HttpUrl


class Settings(BaseSettings):
    """
    Settings for the application.
    """
    socket_server: AnyUrl = "tcp://127.0.0.1:5000"
    flask_server: HttpUrl = "http://0.0.0.0:5555"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
