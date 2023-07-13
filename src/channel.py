import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY_YouTube')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics,contentDetails').execute()
        self.title: str = self.__channel['items'][0]['snippet']['title']  # название канала
        self.description: str = self.__channel['items'][0]['snippet']['description']  # описание канала
        self.url = f'https://www.youtube.com/channel/{channel_id}'  # ссылка на канал
        self.subscriber_count: str = self.__channel['items'][0]['statistics']['subscriberCount']  # количество подписч
        self.video_count: str = self.__channel['items'][0]['statistics']['videoCount']  # количество видео
        self.view_count: str = self.__channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel

    @channel_id.setter
    def channel_id(self, __channel):
        print("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    @classmethod
    def get_service(cls):
        """
        Кл-метод, возвращающий объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_name):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        result = {
            '__channel': self.__channel,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(file_name, "w", encoding='utf8') as json_file:
            json.dump(result, json_file, ensure_ascii=False)
