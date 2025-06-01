from flask import Flask, request, abort
import os

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

# OPENAI_APIKEY = os.getenv("API_KEY")
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET= os.getenv("YOUR_CHANNEL_SECRET")

app = Flask(__name__)

# アクセストークンとWebhookハンドラを設定
configuration = Configuration(access_token=YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_worlda():
    return "a"

@app.route("/callback", methods=['POST'])
def callback():
    # 署名取得
    signature = request.headers['X-Line-Signature']
    # Jsonリクエストを文字列として取得
    body = request.get_data(as_text=True)

    try:
        # handlerにbody,signatureを送りイベントを起こす
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# イベントが起きた時に実行するように登録
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 設定したconfiguration
    with ApiClient(configuration) as api_client:
        # インスタンス作成
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

# if __name__ == '__main__':
#     app.run(port=5100)
