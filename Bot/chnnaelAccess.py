from telebot import *
from variables import token
from threading import Thread
from telebot.apihelper import ApiTelegramException

from api import *

# channelId = ""
channelId = channelId
bot = TeleBot(token)

'''
________________________________________________________________
User methods
'''

def createInvteLink():
    link = bot.create_chat_invite_link(chat_id=channelId,
                                       creates_join_request=True)
    # print(link)
    return link

def getAccess(uId: int):
    user = getUser(uId)
    if user == None:
        bot.decline_chat_join_request(chat_id=channelId, user_id=uId)
        return False
    # if user.isActive:
    #     bot.approve_chat_join_request(chat_id=channelId, user_id=uId)
    #     return True
    elif user.subscriptionEndDate > datetime.now():
        try:
            bot.approve_chat_join_request(chat_id=channelId, user_id=uId)
        except ApiTelegramException:
            return False
        return True
    else:
        bot.decline_chat_join_request(chat_id=channelId, user_id=uId)
        return False

def banChatMember(uId: int):
    def thBan(uId):
        bot.ban_chat_member(chat_id=channelId, user_id=uId)
        time.sleep(5)
        bot.unban_chat_member(chat_id=channelId, user_id=uId, only_if_banned=True)

    thread = Thread(target=thBan, args=[uId])
    thread.start()
