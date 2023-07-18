from src.channel import Channel


class Video(Channel):

    def __init__(self, video_id: str):
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.video = self.get_service().videos().list(id=video_id, part='snippet,contentDetails,statistics').execute()
        self.title: str = self.video['items'][0]['snippet']['title']  # название видео
        self.url = f'https://www.youtube.com/video/{video_id}'  # ссылка на видео
        self.view_count: str = self.video['items'][0]['statistics']['viewCount']  # количество просмотров
        self.like_count: str = self.video['items'][0]['statistics']['likeCount']  # количество лайков

class PLVideo(Video):
    def __init__(self, video_id: str, play_list_id: str):
        super().__init__(video_id)
        self.play_list = self.get_service().playlistItems().list(part="snippet,contentDetails", maxResults=25,
                                                                 playlistId=play_list_id, videoId=video_id).execute()

