from telebot import *
from threading import Thread
from telebot.apihelper import ApiTelegramException

from LounaAdmin.conf import TOKEN_BOT
channelId = "-1001821379673"
bot = TeleBot(TOKEN_BOT)

'''
________________________________________________________________

User methods
'''

def createInvteLink():
    link = bot.create_chat_invite_link(chat_id=channelId,
                                       creates_join_request=True)

    return link.invite_link

def banChatMember(uId: int):
    def thBan(uId):
        bot.ban_chat_member(chat_id=channelId, user_id=uId)
        time.sleep(5)
        bot.unban_chat_member(chat_id=channelId, user_id=uId, only_if_banned=True)

    thread = Thread(target=thBan, args=[uId])
    thread.start()