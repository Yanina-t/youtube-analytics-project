import isodate
from datetime import timedelta
from operator import itemgetter
from src.yt_mixin import YTMixin


class PlayList(YTMixin):
    """Класс для работы в плейлистами ютуб."""

    def __init__(self, playlist_id: str):
        """
        Экземпляр инициализируется id канала и имеет публичные атрибуты.
        """
        self.__playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(part="snippet,contentDetails",
                                                            id=playlist_id,
                                                            maxResults=50, ).execute()
        self.title: str = self.playlist['items'][0]['snippet']['title']  # название плейлиста
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'  # ссылка на плейлист
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50, ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                     self.playlist_videos['items']]  # Получить все id видеороликов из плейлиста
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(
                                                                   self.video_ids)).execute()  # Вывести длительности
        # видеороликов из плейлиста, хранит всю инф о плейлистах

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

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
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
        url_sort = sorted(link_list, key=itemgetter('likeCount'), reverse=True)
        return url_sort[0]['url']
