#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with flask
# It echoes any incoming text messages and does not use the polling method.

import flask
import telebot
import logging

API_TOKEN = '494695462:AAGcy3v-4V3haIWQBWs8gxPPJk_pw9322jM'
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return "This is a redes example"


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Bienvenido al bot del ejemplo de OpenStack. Este bot esta corriendo en OpenStack."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)