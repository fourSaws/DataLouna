from telebot import *
from variables import token

from telebot.types import (
    InputMediaPhoto,
    InputMediaAudio,
    InputMediaVideo,
)
from telebot.apihelper import ApiTelegramException

from urllib.request import urlopen


"""
title - заголовок рассылки
text - текст рассылки
users - массив chat_id пользователей
mediaLinks - ссылки на файлы (разрешены файлы только одного типа)
mediaType - тип файлов (1 - картинка, 2 - аудио, 3 - видео)
"""


def one_timeMailing(title: str, text: str, users: list[int], mediaLinks: list[str] = None, mediaType: int = 0):
    bot = TeleBot(token)
    # if users == None:
    #     users = bot.
    # 986732600
    print("One time mailing")
    # a = urlopen("https://upload.wikimedia.org/wikipedia/commons/3/3c/IMG_logo_%282017%29.svg").read()
    # b = urlopen("https://upload.wikimedia.org/wikipedia/commons/3/3c/IMG_logo_%282017%29.svg").read()
    # z = InputMediaPhoto(a)
    # x = InputMediaPhoto(b)
    # arr:[InputMediaPhoto] = [z, x]

    if len(users) == 0:
        return
    if mediaLinks:
        if text and title:
            return
        message = f'*{title}*\n\n{text}'
        for user in users:
            try:
                bot.send_message(chat_id=user, text=message, parse_mode="Markdown")
            except ApiTelegramException as e:
                print(f'{user} --- {e}')
        return
    media = []
    if mediaType == 0:
        return

    if len(mediaLinks) > 10:
        return

    message = f'*{title}*\n\n{text}'
    if text == None and title == None:
        message = None

    if len(mediaLinks) == 1:
        if mediaType == 1:  # img
            if message == None:
                for user in users:
                    bot.send_photo(user, media[0])
            else:
                for user in users:
                    bot.send_photo(user, media[0], caption=message, parse_mode="Markdown")
        elif mediaType == 2:  # audio
            if message == None:
                for user in users:
                    bot.send_audio(user, media[0])
            else:
                for user in users:
                    bot.send_audio(user, media[0], caption=message, parse_mode="Markdown")
        elif mediaType == 3:  # video
            if message == None:
                for user in users:
                    bot.send_video(user, media[0])
            else:
                for user in users:
                    bot.send_video(user, media[0], caption=message, parse_mode="Markdown")
        return

    if mediaType == 1:  # img
        for imgPath in mediaLinks[0:-1]:
            media.append(InputMediaPhoto(imgPath))
        if message == None:
            media.append(InputMediaPhoto(mediaLinks[-1]))
        else:
            media.append(InputMediaPhoto(mediaLinks[-1], caption=message, parse_mode="Markdown"))
    elif mediaType == 2:  # audio
        for imgPath in mediaLinks[0:-1]:
            media.append(InputMediaAudio(imgPath))
        if message == None:
            media.append(InputMediaAudio(mediaLinks[-1]))
        else:
            media.append(InputMediaAudio(mediaLinks[-1], caption=message, parse_mode="Markdown"))
    elif mediaType == 3:  # video
        for imgPath in mediaLinks[0:-1]:
            media.append(InputMediaVideo(imgPath))
        if message == None:
            media.append(InputMediaVideo(mediaLinks[-1]))
        else:
            media.append(InputMediaVideo(mediaLinks[-1], caption=message, parse_mode="Markdown"))

    for user in users:
        try:
            bot.send_media_group(chat_id=user, media=media)
        except ApiTelegramException as e:
            print(f'{user} --- {e}')
    return
    # bot.send_media_group(chat_id=986732600, media=media)
    # return
