from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

# 填入你的 Line Channel Access Token
line_bot_api = LineBotApi('I86eRgDQEGoKvT5aXoefw9ekgJ4z2ACVKABcl9FK/JO1zbkWtwEYSjdzITlNNqSk0deRWhWVKGe3BvCef35jz7EDmBZVHTleu5/98I1CDuHP1IvglHx8t2YoT6WIu2Ica2E3TtEoftaprwIlEv4LOAdB04t89/1O/w1cDnyilFU=')

# 填入你的 Line Channel Secret
handler = WebhookHandler('c22f27f77d5d23fe3265b82966e7b02d')

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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run()
