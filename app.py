from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import random

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['xpxTa3kRpJbqrTTNX95Clsc049UgbM2lULufHj6jGqc90H11P0F/iznIVmoK9xQz0deRWhWVKGe3BvCef35jz7EDmBZVHTleu5/98I1CDuElovM4oS4hWAQ95c61fpPCVly+ZaHxXh5UJWrsQf5XPwdB04t89/1O/w1cDnyilFU='])
handler = WebhookHandler(os.environ['3303784f32f830283e4da4267f095e7a'])

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
    msg = event.message.text
    if msg == "點歌":
        song_list = ['歌曲1', '歌曲2', '歌曲3', '歌曲4', '歌曲5']
        reply_msg = TextSendMessage(text=random.choice(song_list))
    else:
        reply_msg = TextSendMessage(text="請輸入「點歌」來點一首歌曲！")

    line_bot_api.reply_message(event.reply_token, reply_msg)

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
