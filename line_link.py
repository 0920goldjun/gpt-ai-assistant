from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 填入你的Channel Access Token
line_bot_api = LineBotApi('7pmZq5RU907oot52B1fwl7UAv3Nsi5mI0jhV9OlUZVqP9eY8yyY9vAD/NSuBYaClIkX+B5Ver0il3Carh1VevXzvxD8SYCEEYs+WAgO2AtuquCFr9HrzUdHbiiNCRzOmfp3P01JbS5qzV/eeaopkXAdB04t89/1O/w1cDnyilFU=')
# 填入你的Channel Secret
handler = WebhookHandler('c58244b4c385cc6a195d9231af7a48d0')

# 設定Webhook路徑與方法
@app.route("/callback", methods=['POST'])
def callback():
    # 獲取Header中的資訊
    signature = request.headers['X-Line-Signature']
    # 獲取使用者傳送的訊息內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        # 解析訊息是否為LINE平台發送的合法訊息
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 不合法訊息則回傳400
        abort(400)

    return 'OK'

# 設定訊息回覆
@handler.add(MessageEvent, message=TextMessage)
def reply_message(event):
    # 回覆使用者發送的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    # 開始運行Flask應用程式
    app.run()
