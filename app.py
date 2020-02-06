from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from bs4 import BeautifulSoup
import requests
import config
import json

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Command Handlers. Usually take two arguments: bot and update.


class Bot:
    def __init__(self):
        self.job = None
        updater = Updater(
            token=config.TOKEN, use_context=True)
        # Get dispatcher to register handlers
        dispatcher = updater.dispatcher
        # answer commands
        # dispatcher.add_handler(CommandHandler(
        #    'set_interval', self.set_interval, pass_args=True))
        dispatcher.add_handler(CommandHandler('help', self.client_help))
        dispatcher.add_handler(CommandHandler('start', self.start))
        #dispatcher.add_handler(CommandHandler('stop', self.stop))
        # start the bot
        updater.start_polling()
        # Stop
        updater.idle()

    def send_updates(self, context):
        res = requests.get(
            "https://bnonews.com/index.php/2020/02/the-latest-coronavirus-cases/")
        soup = BeautifulSoup(res.content, "html.parser")

        table = soup.find_all("table")[0]
        rows = table.find_all("tr")
        row = rows[len(rows)-1]

        text = 'Latest updates on the outbreak\n\n'
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

    def start(self, update, context):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Welcome! You initiated the Bot. Now you will be receiving the list of infected countries and the number of infected/dead people there.\nUse <code>/help</code> to look up commands.\nDeveloped by @rcbxd 😊',
                                 parse_mode='HTML')

        context.job_queue.run_repeating(
            self.send_updates, interval=3600, first=1, context=update.message.chat_id)

    def client_help(self, update, context):
        text = "<strong>Help</strong>\n\n"
        text = text + "Commands: \n"
        text = text + \
            " - <code>/start</code> - starts the bot (15 minute interval).\n"
        text = text + \
            " - <code>/set_interval + time in seconds</code> - lets you set the interval on your own.\n"
        text = text + " - <code>/stop</code> - stops sending the statistics.\n\n"

        text = text + "Developed by <strong>rcbxd</strong> 😊\n"
        text = text + "Read about the <a href=\"https://en.wikipedia.org/wiki/2019%E2%80%9320_Wuhan_coronavirus_outbreak\">coronavirus</a>."

        context.bot.send_message(
            chat_id=update.message.chat_id, text=text, parse_mode='HTML')


'''
    def set_interval(self, update, context):
        if (context.job_queue):
            if (context.args):
                context.job_queue.run_once(
                    self.remove_job, 0.01, context=update.message.chat_id)
                context.job_queue.run_repeating(
                    self.send_updates, interval=int(context.args[0]), first=1, context=update.message.chat_id)
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'You\'ve changed the job interval to {context.args[0]} seconds.')
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text='Please provide the interval in the following format: <code>/set_interval your_number_in_seconds</code>',
                                         parse_mode='HTML')
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text='You need to start the bot first, run <code>/start</code> to do that.',
                                     parse_mode='HTML')

    def remove_job(self, context):
        context.job.stop()
'''


'''
    def stop(self, update, context):
        if (context.job_queue):
            context.job_queue.run_once(
                self.remove_job, 0, context=update.message.chat_id)
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="You've stopped the job. To start again run either <code>/set_interval</code> or <code>/start</code>", parse_mode='HTML')
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='You need to start the bot first, run <code>/start</code> to do that.',
                                     parse_mode='HTML')
'''

if __name__ == '__main__':
    Bot()
