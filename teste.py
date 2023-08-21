from pytube import YouTube

def get_video_info(url):
    try:
        video = YouTube(url)

        video_data = {
            'title': video.title,
            'channel': video.author,
            'views': video.views,
            'thumbnail': video.thumbnail_url,
        }

        return video_data
    except Exception as e:
        print(f"Erro ao obter informações do vídeo: {e}")
        return None

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=bBuU1efnfUM'  # Substitua pela URL do vídeo que você quer obter informações

    video_info = get_video_info(video_url)
    if video_info:
        print(video_info['rating'])