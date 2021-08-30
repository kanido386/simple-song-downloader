# -*- coding: utf-8 -*-
# the code is copied from my previous project

import json
import os
from googleapiclient.discovery import build

class YoutubeAgent(object):
    ''' 抓 YouTube 影片的網址 '''

    def __init__(self, tracks, txt_file):
        self.youtube = None
        self.tracks = tracks
        self.song_list = []
        self.txt_file = txt_file

        self.init_youtube()
        self.init_song_list_with_txt()
        self.add_tracks_to_song_list()
        self.save_song_list()


    def init_youtube(self):
        youTubeApiKey = os.environ.get("YOUTUBE_API_KEY")
        self.youtube = build('youtube', 'v3', developerKey=youTubeApiKey)


    def init_song_list_with_txt(self):
        # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        if not os.path.exists(self.txt_file):
            with open(self.txt_file, 'w'):
                return

        # TODO: 如果 data.txt 是空的會出錯！
        with open(self.txt_file) as json_file:
            song_list = json.load(json_file)
            for item in song_list:
                artist, song, videoUrl = item
                self.song_list.append((artist, song, videoUrl))



    def add_tracks_to_song_list(self):
        # 用下面的 list 來判別有無重複
        artist_song_list = [f'{item[0]} - {item[1]}' for item in self.song_list]

        for artist, song in self.tracks:
            if f'{artist} - {song}' in artist_song_list:
                continue

        # 想抓「某某」歌 => 用「某某 lyrics」當關鍵詞搜尋 YouTube => 找最相關的影片當作目標
        request = self.youtube.search().list(
            part='snippet',
            q=f'{artist} {song} lyrics',
            type='video'
        )
        response = request.execute()
        # The video that is most relevant to the search query
        firstVideo = response['items'][0]
        videoId = firstVideo['id']['videoId']
        videoUrl = f'https://www.youtube.com/watch?v={videoId}'
        self.song_list.append((artist, song, videoUrl))
        # 邊處理邊印出，讓使用者有被回饋的感覺！
        print(f'{artist} - {song}')
        print('影片網址:', videoUrl)
        print('==============================')


    def print_song_list(self):
        for artist, song, videoUrl in self.song_list:
            print(f'{artist} - {song}')
            print('影片網址:', videoUrl)
            print('==============================')


    def get_song_list(self):
        return self.song_list


    def save_song_list(self):
        # https://pythonexamples.org/python-list-to-json/
        with open(self.txt_file, 'w', encoding='utf-8') as outfile:
            # http://litaotju.github.io/python/2016/06/28/python-json-dump-utf/
            json.dump(self.song_list, outfile, ensure_ascii=False)