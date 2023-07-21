from datetime import timedelta
from operator import itemgetter

import isodate

from src.API_KEY_YT import youtube


class PlayList:
    def __init__(self, playlist_id: str):
        """
        Экземпляр инициализируется id канала и имеет публичные атрибуты.
        """
        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(part="snippet,contentDetails",
                                                 id=playlist_id,
                                                 maxResults=50, ).execute()
        self.title: str = self.playlist['items'][0]['snippet']['title']  # название плейлиста
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'  # ссылка на плейлист
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50, ).execute()

    @property
    def video_ids(self):
        """
        Получить все id видеороликов из плейлиста
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        return video_ids

    @property
    def video_response(self):
        """
        Вывести длительности видеороликов из плейлиста, хранит всю инф о плейлистах
        """
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)).execute()
        return video_response

    def video_duration(self):
        """
        Получаем список длительности времени по каждому видео и сохраняем в список all_time
        """
        all_time = []
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_time.append(duration)
        return all_time

    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность
        плейлиста (обращение как к свойству, использовать @property)
        """
        total_duration = sum(self.video_duration(), timedelta())
        return total_duration

    def total_seconds(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительностью секунд плейлиста
        """
        total_seconds = sum(self.video_duration(), timedelta())
        return total_seconds.seconds

    @property
    def list_for_best_video(self):
        """
        Возвращает список видео из плейлиста (по количеству лайков, id, url)
        """
        link_list = []
        for video in self.video_response['items']:
            vid_like = video['statistics']['likeCount']
            vid_id = video['id']
            yt_link = f'https://youtu.be/{vid_id}'
            link_list.append(
                {
                    'likeCount': int(vid_like),
                    'url': yt_link
                }
            )
        return link_list

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        url_sort = sorted(self.list_for_best_video, key=itemgetter('likeCount'), reverse=True)
        return url_sort[0]['url']
