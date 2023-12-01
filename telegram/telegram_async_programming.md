# 🎉 Telegram Async Process
> Telegram API 이해를 위한 문서 입니다.   

### 1️⃣ 기본 사용법     
```
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 봇 토큰을 설정합니다.
TOKEN = 'your_bot_token'
updater = Updater(token=TOKEN, use_context=True)

# /start 명령어 핸들러 함수
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('안녕하세요! 봇이 시작되었습니다.')

# /help 명령어 핸들러 함수
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('도움말을 표시합니다.')

# 명령어 핸들러를 봇에 추가합니다.
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help_command))

# 봇을 시작합니다.
updater.start_polling()

# 봇이 계속 실행되도록 유지합니다.
updater.idle()

```
|Method|기능|
|--|--|
|Updater  |텔레그램 봇과 텔레그램 서버 간의 통신을 관리하고 업데이트를 수신|
|Update |텔레그램에서 오는 모든 업데이트(메시지, 채팅 상태 변경, 새로운 멤버 등)를 수신|
|CommandHandler |텔레그램에서 오는 모든 업데이트(메시지, 채팅 상태 변경, 새로운 멤버 등)를 수신|
|CallbackContext |이벤트 핸들러 함수에 CallbackContext를 사용하여 콜백 데이터를 전달<br>비동기 작업을 수행 후 작업이 완료시 작업의 결과를 통해 추가적인 동작을 수행|

### 2️⃣ 비동기 프로그래밍
> 파이썬에서 텔레그램 API를 사용하여 텔레그램에 메시지를 보낼 때 비동기로 작성해야 한다
#### 🤔 Why? 
* 응답 대기 시간 해소
  + 텔레그램 API 호출은 외부 서버와의 통신을 필요로 하며, 텔레그램 API는 메시지를 송수신하고 알람만 보내는 등   
    네트워크 요청이 잦습니다.   
  + 비동기 방식을 사용하면 네트워크 요청을 기다리는 동안 다른 작업을 수행할 수 있어  
    프로그램이 더 효율적으로 동작할 수 있습니다.
* 다중 요청 관리:
  + 비동기 작업을 사용하면 여러 개의 API 호출을 동시에 수행할 수 있습니다.
  + 동기적인 방식에서는 한 번에 하나의 API 호출만 처리할 수 있어 여러 요청을 동시에   
    처리하기 위해서는 별도의 쓰레드나 프로세스를 사용해야 합니다.

