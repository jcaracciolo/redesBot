#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File to setup Telegrams webHook

import telebot
import time

API_TOKEN = '494695462:AAGcy3v-4V3haIWQBWs8gxPPJk_pw9322jM'

WEBHOOK_HOST = 'itba-telegram-bot.herokuapp.com'

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private keyheroku open


# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s" % (WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

bot = telebot.TeleBot(API_TOKEN)
print("Cleaning webhook")
bot.remove_webhook()
print("webhook cleaned")
time.sleep(10)
print("Setting webhook")
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)
print("webhook set")