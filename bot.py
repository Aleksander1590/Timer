import telebot
from dotenv import load_dotenv
import os
import time
from pytimeparse import parse

load_dotenv()

TG_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TG_TOKEN:
    raise ValueError("Не найден TELEGRAM_TOKEN в переменных окружения!")

bot = telebot.TeleBot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(chat_id, secs_left):
    progress_msg = bot.send_message(chat_id, f"Запуск таймера на {secs_left} секунд...")
    for remaining in range(secs_left, -1, -1):
        progress_bar = render_progressbar(secs_left, remaining)
        bot.edit_message_text(f"Осталось {remaining} секунд {progress_bar}", chat_id, progress_msg.message_id)
        if remaining == 0:
            bot.send_message(chat_id, "Время вышло!")
        time.sleep(1)


def choose(message):
    user_input = message.text.strip()
    delay = parse(user_input)
    if delay is not None and delay > 0:
        notify_progress(message.chat.id, delay)


def main():
    @bot.message_handler(content_types=['text'])
    def handle_message(message):
        choose(message)
    bot.polling()


if __name__ == "__main__":
    main()
    
