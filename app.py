from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import random
import requests

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['656cb267b52976f0712221a0e7671e26'])

# YouTube Music API 相關資訊
YTM_API_KEY = os.environ['YTM_API_KEY']
YTM_API_BASE_URL = 'https://www.googleapis.com/youtube/v3'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '點歌':
        songs = search_songs('歌曲')  # 使用歌曲關鍵字進行搜尋，這裡可以根據需求進行調整
        if songs:
            song = random.choice(songs)
            message = TextSendMessage(text='為您點播的歌曲是：{}\n歌手：{}'.format(song['title'], song['artist']))
        else:
            message = TextSendMessage(text='找不到符合條件的歌曲')
    else:
        message = TextSendMessage(text='請輸入「點歌」來點播歌曲')
    
    line_bot_api.reply_message(event.reply_token, message)


def search_songs(keyword):
    url = f"{YTM_API_BASE_URL}/search"
    params = {
        'key': YTM_API_KEY,
        'part': 'snippet',
        'q': keyword,
        'type': 'video',
        'maxResults': 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    songs = []
    for item in data['items']:
        song = {
            'title': item['snippet']['title'],
            'artist': item['snippet']['channelTitle'],
            'videoId': item['id']['videoId']
        }
        songs.append(song)

    return songs


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
