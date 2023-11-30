import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start 메시지 전송
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("모드를 선택해 주세요 :)\n 1. 거북목 모드 \n2. 척추측만증 모드")

#    /set 명령어를 통해 타이머를 설정하고, 설정한 시간이 경과하면 alarm 함수가 실행되도록 하는 기능을 제공
async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    try:
        due = float(context.args[0])
        if due == 1:
            text = "거북목 모드 설정이 완료됐어요!"
            await update.effective_message.reply_text(text)
            return
        elif due == 2:
            text = "척추측만증 모드 설정이 완료됐어요!"
            await update.effective_message.reply_text(text)
            return
        else:
            await update.message.reply_text("1 또는 2를 입력해주세요 :) ")
            return

    except (IndexError, ValueError):
        await update.effective_message.reply_text("1 또는 2를 입력해주세요 :) ")

        
# /unset : 종료함수
async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("프로그램이 종료 되었습니다.")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6819441562:AAGTiWeoinUOE3W22M0L3R7u4CErKWSMzTw").build()
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_mode))
    application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()