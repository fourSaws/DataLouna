import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import django

from DataLounaNotifications.chnnaelAccess import createInvteLink

django.setup()
from LounaAdmin import onetimeMailing
from DataLounaNotifications.models import *
from LounaAdmin.models import User


def updateStatusPaymentDeclied(site_id):
    user_check = User.objects.get(site_id=site_id)
    text_first = EventsNotifications.objects.get(notifications_id=6).text
    user = [user_check.chat_id]
    time.sleep(3600)
    onetimeMailing.one_timeMailing(text=text_first, users=user)
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="✅ Получить прогнозы",
            callback_data="3214"  # TODO: Вставить ссылку на сайт
        )
    )
    text_second = EventsNotifications.objects.get(notifications_id=7).text
    time.sleep(15)
    onetimeMailing.quiz(markup=btn, text=text_second, users=user)


def onEnterFirst(user_exists=None, site_id=None, status_=None, chat_id=None):
    user_exists.site_id = site_id
    user_exists.subscription_status = status_
    user_exists.save()
    notification = EventsNotifications.objects.get(notifications_id=2)
    title = notification.title
    text = notification.text
    user = [chat_id]
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="💳  Оформить подписку",
            callback_data='123'
        )
    )
    time.sleep(20)
    onetimeMailing.quiz(title=title, text=text, markup=markup, users=user)


def onEnterSecond(user_exists=None, site_id=None, status_=None, chat_id=None):
    notification = EventsNotifications.objects.get(notifications_id=3)
    user_exists.site_id = site_id
    user_exists.subscription_status = status_
    user_exists.save()
    title = notification.title
    text = f"{notification.text} \n {user_exists.subscription_end_date[:10]}"
    user = [chat_id]
    onetimeMailing.one_timeMailing(title=title, text=text, users=user)


def onEnterSecondAndDateTime(user_exists=None, site_id=None, status_=None, chat_id=None):
    notification = EventsNotifications.objects.get(notifications_id=4)
    user_exists.site_id = site_id
    user_exists.subscription_status = status_
    user_exists.save()
    title = notification.title
    text = notification.text
    user = [chat_id]
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text=" 💳  Оформить подписку",
            callback_data='123'  # TODO:Редирект на оплату
        )
    )
    onetimeMailing.quiz(title=title, text=text, markup=markup, users=user)


def onEnterThird(user_exists=None, site_id=None, status_=None, chat_id=None, subscription_end_date=None):
    notification = EventsNotifications.objects.get(notifications_id=5)
    title = notification.title
    user_exists.site_id = site_id
    user_exists.subscription_status = status_
    user_exists.subscription_end_date = subscription_end_date
    user_exists.save()
    text = f"{notification.text} \n {user_exists.subscription_end_date[:10]}"
    user = [chat_id]
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Вступить в приватный канал",
            url=createInvteLink()

        )
    )
    time.sleep(20)
    onetimeMailing.quiz(title=title, text=text, users=user, markup=markup)
