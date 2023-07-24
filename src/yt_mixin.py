import os
from googleapiclient.discovery import build


class YTMixin:
    api_key: str = os.getenv('API_KEY_YouTube')

    @classmethod
    def get_service(cls):
        """
        Кл-метод, возвращающий объект для работы с YouTube API
        """
        return build('youtube', 'v3', developerKey=cls.api_key)
