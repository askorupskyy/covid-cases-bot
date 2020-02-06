from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from bs4 import BeautifulSoup
import requests
import config

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Command Handlers. Usually take two arguments: bot and update.


def send_updates(context):
    res = requests.get(
        "https://bnonews.com/index.php/2020/02/the-latest-coronavirus-cases/")
    soup = BeautifulSoup(res.content, "html.parser")

    table = soup.find_all("table")[0]
    rows = table.find_all("tr")
    row = rows[len(rows)-1]

    text = 'Latest updates on the <a href=\"https://en.wikipedia.org/wiki/2019%E2%80%9320_Wuhan_coronavirus_outbreak\">coronavirus</a> outbreak\n\n'
    text = text + \
        f'<code>China -> \t\t{row.find_all("strong")[1].get_text()}/{row.find_all("strong")[2].get_text()}\n'

    table = soup.find_all("table")[2]
    rows = table.find_all("tr")[1:-1]

    for c in rows:
        country = c.find_all("td")[0].get_text()
        cases = c.find_all("td")[1].get_text()
        dead = c.find_all("td")[2].get_text()
        text = text + country + " -> \t\t"
        text = text + cases + "/"
        text = text + dead + "\n"

    context.bot.send_message(
        chat_id=context.job.context,
        text=text + "</code>", parse_mode='HTML'
    )


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Welcome! Now you will receive updates on coronavirus (nCov2019) every 30 seconds!')

    context.job_queue.run_repeating(
        send_updates, interval=900, first=0, context=update.message.chat_id)


def main():
    # Create updater and pass in Bot's auth key.
    updater = Updater(
        token=config.TOKEN, use_context=True)
    # Get dispatcher to register handlers
    dispatcher = updater.dispatcher
    # answer commands
    dispatcher.add_handler(CommandHandler('start', start))
    # start the bot
    updater.start_polling()
    # Stop
    updater.idle()


if __name__ == '__main__':
    main()
