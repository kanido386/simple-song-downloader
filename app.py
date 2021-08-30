import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import webbrowser
# from youtube_agent import YoutubeAgent
from googleapiclient.discovery import build
from werkzeug.utils import redirect

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")


@app.route("/download", methods=["POST","GET"])
def download():

    artist = request.form["artist"]
    song = request.form["song"]

    # TODO:
    # https://www.youtube.com/results?search_query=bruno+mars+grenade+lyrics
    # https://www.youtube.com/results?search_query=王藍茵 惡作劇

    youTubeApiKey = os.environ.get("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=youTubeApiKey)

    # 想抓「某某」歌 => 用「某某 lyrics」當關鍵詞搜尋 YouTube => 找最相關的影片當作目標
    req = youtube.search().list(
        part='snippet',
        q=f'{artist} {song} lyrics',
        type='video'
    )
    res = req.execute()
    # The video that is most relevant to the search query
    firstVideo = res['items'][0]
    videoId = firstVideo['id']['videoId']
    videoUrl = f'https://www.youtube.com/watch?v={videoId}'

    temp = videoUrl.split('youtube')
    downloadUrl = f'{temp[0]}backupmp3{temp[1]}'
    
    return render_template("download.html", downloadUrl=downloadUrl)


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)