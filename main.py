#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with flask
# It echoes any incoming text messages and does not use the polling method.

import flask
from flask import send_from_directory
import telebot
from telebot import types
import redis
import logging
import commands

API_TOKEN = '613516960:AAFw5oWewRPeucTgRxHXhF7ZMnbdbUJ8Z7w'
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

descPrefix = "desc_"
statePrefix = "state_"

"""
REDIS FUNCTIONS
"""
def descKey(user, index):
    return descPrefix + str(user) + str(index)

def stateKey(user, index):
    return statePrefix + str(user) + str(index)

def keyList(user):
    return redis.keys(pattern=(descPrefix + str(user) + "*"))

def eventCount(user):
    return len(keyList(user))

def addEvent(user, desc):
    nextIndex = eventCount(user) + 1
    redis.set(descKey(user, nextIndex), desc)
    redis.set(stateKey(user, nextIndex), "TODO")
    return nextIndex

def getState(user, index):
    return redis.get(stateKey(user,index))

def setState(user, index, newState):
    redis.set(stateKey(user, index), newState)

def getDescription(user, index):
    return redis.get(descKey(user,index))

def getAllEvents(user):
    ans = []
    for k in keyList(user):
        ans.append((k.replace(descPrefix + str(user),"",1), redis.get(k), redis.get(k.replace(descPrefix, statePrefix))))
    return sorted(ans, key=lambda tuple: tuple[0])
"""
END OF REDIS FUNCTIONS
"""


"""
OTHER FUNCTIONS
"""
def validate(message, user, id):
    if not id.isdigit():
        bot.send_message(chat_id=message.chat.id,
                         text=str(id) + " no es un numero de actividad valido")
        return False

    if getDescription(user, id) == None:
        bot.send_message(chat_id=message.chat.id,
                         text=str(id) + " no es un id de actividad, para ver la lista de actividades usar /list")
        return False
    return True
"""
END OF OTHER FUNCTIONS
"""
redis.set("TESTING_KEY", "ALLGOOD")
# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return send_from_directory('.','main.html')


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
    print(dir(message.chat))
    bot.send_message(chat_id=message.chat.id,
                 text=("Bienvenido al bot del ejemplo de OpenStack. Este bot esta corriendo en OpenStack. \n"
                  "- Sere responsable de tomar tu lista de cosas para hacer. \n"
                  "- Por favor agrega algo usando el comando /add <descripcion del evento> \n"
                  "- Si deseas ver tus cosas por hacer usa el comando /list \n"
                  "- Si quieres ver las cosas que ya terminaste usa el comando /donelist \n"
                  "- Todo evento comenzara en estado TODO, si desea updetear el estado usa /update <eventID> <Nuevo estado> \n"
                  "- Si deseas marcar un evento como terminado usa /done <eventID> \n"))

@bot.message_handler(commands=['add'])
def send_welcome(message):
    text = message.text.replace("/add ","",1)
    addEvent(message.from_user.id, text)
    bot.send_message(chat_id=message.chat.id,
                 text=text + " added")


@bot.message_handler(commands=['list'])
def send_welcome(message):
    events = getAllEvents(message.from_user.id)
    text = ""
    for (i, e, s) in events:
        if s.lower() != "done":
            text += i + ") " + e + "\t - " + s + "\n"
    bot.send_message(chat_id=message.chat.id,
                 text="Tu lista de cosas por hacer es: \n" + text)

@bot.message_handler(commands=['done'])
def send_welcome(message):
    id = message.text.replace("/done ", "", 1)
    user = message.from_user.id
    if validate(message, user, id):
        if getState(user, id) == "done":
            bot.send_message(chat_id=message.chat.id,
                             text="La actividad < " + getDescription(user,id) + " > ya estaba marcada como terminada")
        else:
            setState(user, id, "done")
            bot.send_message(chat_id=message.chat.id,
                             text="Felicitaciones la actividad < " + getDescription(user, id) + "  > fue marcada como terminada")

@bot.message_handler(commands=['update'])
def send_welcome(message):
    id, state = message.text.replace("/update ","",1).split(" ", 1)
    user = message.from_user.id
    if validate(message, user, id):
        if getState(user, id) == "done":
            setState(user, id, state)
            bot.send_message(chat_id=message.chat.id,
                             text="La actividad < " + getDescription(user,id) + " > ya estaba marcada como terminada,"
                                                                                " pero fue actualizada a < " +
                             getState(user, id) + " >")
        else:
            setState(user, id, state)
            bot.send_message(chat_id=message.chat.id,
                             text="La actividad < " + getDescription(user, id) + "  > fue actualizada a < " +
                             getState(user, id) + " >")

@bot.message_handler(commands=['donelist'])
def send_welcome(message):
    events = getAllEvents(message.from_user.id)
    text = ""
    for (i, e, s) in events:
        if s.lower() == "done":
            text += i + ") " + e + "\t - " + s + "\n"
    bot.send_message(chat_id=message.chat.id,
                 text="Tu lista de cosas que terminaste es: \n" + text)

@bot.message_handler(commands=['run'])
def send_welcome(message):
    password, code = id, state = message.text.replace("/run ","",1).split(" ", 1)
    if password != "sudosecret":
      bot.send_message(chat_id=message.chat.id,
                   text="La contraseña provista es incorrecta")
    else:
      ans = commands.getstatusoutput(code)
      bot.send_message(chat_id=message.chat.id,
                   text=ans[1])



# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)