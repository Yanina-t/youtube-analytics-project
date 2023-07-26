from src.yt_mixin import YTMixin


class Video(YTMixin):

    def __init__(self, video_id: str):
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.video = self.get_service().videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()
        try:
            self.title: str = self.video['items'][0]['snippet']['title']  # название видео
            self.url = f'https://www.youtube.com/video/{video_id}'  # ссылка на видео
            self.view_count: str = self.video['items'][0]['statistics']['viewCount']  # количество просмотров
            self.like_count: str = self.video['items'][0]['statistics']['likeCount']  # количество лайков
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id: str, play_list_id: str):
        super().__init__(video_id)
        self.play_list = play_list_id
