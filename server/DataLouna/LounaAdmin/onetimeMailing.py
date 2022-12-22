from telebot import *
from .conf import TOKEN_BOT
from telebot.types import (
    InputMediaPhoto,
    InputMediaAudio,
    InputMediaVideo, InlineKeyboardMarkup,
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


def one_timeMailing(
    text: str,
    users: list[int],
    title: str = None,
    mediaLinks: list[str] = None,
    mediaType: int = 0,
):
    bot = TeleBot(TOKEN_BOT)
    print("One time mailing")
    if len(users) == 0:
        return
    if not mediaLinks:
        if not text:
            return
        if title:
            message = f"*{title}*\n\n{text}"
        else:
            message = f"{text}"
        for user in users:
            try:
                bot.send_message(chat_id=user, text=message, parse_mode="Markdown")
            except ApiTelegramException as e:
                print(f"{user} --- {e}")
        return
    media = []
    if mediaType == 0:
        return

    if len(mediaLinks) > 10:
        return

    message = f"*{title}*\n\n{text}"
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
            print(f"{user} --- {e}")
    return


def quiz(text: str, markup: InlineKeyboardMarkup, users: list[int], title: str = None):
    '''
    Функция для рассылки опросов
    :param text: Текст вопроса
    :param markup: Клавиатура опроса класса InlineKeyboardMarkup. У каждой кнопки клавиатуры первый символ "callback_data" должен быть "q"
    :param users: Список id пользователей, которым нужно отправить вопрос
    :return:
    '''
    bot = TeleBot(TOKEN_BOT)
    if title == None:
        for user in users:
            try:
                bot.send_message(chat_id=user,
                                 text=f"{text}",
                                 reply_markup=markup,
                                 parse_mode="Markdown",
                                 )
            except ApiTelegramException as e:
                print(f'{user} --- {e}')
    else:
        for user in users:
            try:
                bot.send_message(chat_id=user,
                                 text=f"*{title}*\n\n{text}",
                                 reply_markup=markup,
                                 parse_mode="Markdown",
                                 )
            except ApiTelegramException as e:
                print(f'{user} --- {e}')
