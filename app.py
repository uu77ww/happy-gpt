from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import random
from ytmusicapi import YTMusic

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['c22f27f77d5d23fe3265b82966e7b02d'])
handler = WebhookHandler(os.environ['656cb267b52976f0712221a0e7671e26'])

yt = YTMusic('oauth.json')

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
        reply_text = '請輸入歌名或歌詞以進行搜尋'
    else:
        reply_text = search_song(event.message.text)
    
    message = TextSendMessage(text=reply_text)
    line_bot_api.reply_message(event.reply_token, message)


def search_song(keyword):
    search_results = yt.search(keyword, filter='songs', limit=1)

    if search_results:
        video_id = search_results[0]['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return f"找到符合條件的歌曲：\n{video_url}"
    else:
        return "找不到符合條件的歌曲"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
