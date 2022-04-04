import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import webbrowser
# from youtube_agent import YoutubeAgent
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")


@app.route("/download", methods=["POST","GET"])
def download():

    artist = request.form["artist"]
    song = request.form["song"]

    # TODO: it looks like youtube blocks the scraping...
    # # https://www.youtube.com/results?search_query=bruno+mars+grenade+lyrics
    # # https://www.youtube.com/results?search_query=王藍茵 惡作劇
    # url = 'https://www.youtube.com/results?search_query=bruno+mars+grenade+lyrics'
    # headers = {'user-agent': 'Mozilla/5.0'}
    # source = requests.get(url, headers=headers)
    # soup = BeautifulSoup(source.text, 'html.parser')
    # urls = soup.find_all('a')
    # print(urls)


    youTubeApiKey = os.environ.get("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=youTubeApiKey)

    # 想抓「某某」歌 => 用「某某 lyrics」當關鍵詞搜尋 YouTube => 找最相關的影片當作目標
    req = youtube.search().list(
        part='snippet',
        q=f'{artist} {song} lyrics',
        type='video'
    )
    res = req.execute()
    # # The video that is most relevant to the search query
    # firstVideo = res['items'][0]
    # videoId = firstVideo['id']['videoId']
    # videoUrl = f'https://www.youtube.com/watch?v={videoId}'
    Videos = res['items'][0:5]
    videoIds = [Videos[i]['id']['videoId'] for i in range(5)]
    videoUrls = [f'https://www.youtube.com/watch?v={videoId}' for videoId in videoIds]

    # https://www.youtube.com/embed/{videoId}
    temps = [videoUrls[i].split('watch?v=') for i in range(5)]
    embedVideoUrls = [f'{temps[i][0]}embed/{temps[i][1]}' for i in range(5)]

    temps = [videoUrls[i].split('youtube') for i in range(5)]
    downloadUrls = [f'{temps[i][0]}backupmp3{temps[i][1]}' for i in range(5)]
    
    return render_template("download.html", embedVideoUrls=embedVideoUrls, downloadUrls=downloadUrls)


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)