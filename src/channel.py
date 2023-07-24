import json
import os

from src.yt_mixin import YTMixin


class Channel(YTMixin):
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY_YouTube')

    def __init__(self, channel_id: str):
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.__channel = self.get_service().channels().list(id=channel_id,
                                                            part='snippet,statistics,contentDetails').execute()
        self.title: str = self.__channel['items'][0]['snippet']['title']  # название канала
        self.description: str = self.__channel['items'][0]['snippet']['description']  # описание канала
        self.url = f'https://www.youtube.com/channel/{channel_id}'  # ссылка на канал
        self.subscriber_count: str = self.__channel['items'][0]['statistics']['subscriberCount']  # количество подписч
        self.video_count: str = self.__channel['items'][0]['statistics']['videoCount']  # количество видео
        self.view_count: str = self.__channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel

    @channel_id.setter
    def channel_id(self, __channel):
        print("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    def to_json(self, file_name):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        result = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(file_name, "w", encoding='utf8') as json_file:
            json.dump(result, json_file, ensure_ascii=False)
