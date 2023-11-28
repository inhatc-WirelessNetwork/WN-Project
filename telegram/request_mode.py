
import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start 메시지 전
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("모드를 선택해 주세요 :)\n 1. 거북목 모드 \n2. 척추측만증 모드")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.sendPhoto(job.chat_id, photo=open("../image.jpg","rb"))


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    print(f"sadasdasas{current_jobs}")

    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

#    /set 명령어를 통해 타이머를 설정하고, 설정한 시간이 경과하면 alarm 함수가 실행되도록 하는 기능을 제공
async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        while True:
            due = float(context.args[0])
            if due == 1:
                text = "거북목 모드 설정이 완료됐어요!"
                await update.effective_message.reply_text(text)
            elif due == 2:
                text = "척추측만증 모드 설정이 완료됐어요!"
                await update.effective_message.reply_text(text)
            else:
                await update.message.reply_text("1 또는 2를 입력해주세요 :) ")
                return
                
            job_removed = remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

            # text = "모드 설정이 완료됐어요!"
            if job_removed:
                text += " Old one was removed."
            await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("1 또는 2를 입력해주세요 :) ")

        

async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    print(f"unset chat_id : {chat_id}" )
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


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
