from datetime import datetime, timedelta

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from DataLounaNotifications.chnnaelAccess import banChatMember
from DataLounaNotifications.models import Quiz, QuizQuestions, QuestionAnswers, EventsNotifications
from LounaAdmin.onetimeMailing import one_timeMailing, quiz
from LounaAdmin.models import NoviceNewsTellers, User

# TODO:Когда буду делать опросы дописать для первого статуса
# users_first = list(i["chat_id"] for i in User.objects.get(subscription_status="FIRST").values('chat_id'))
channelId = "-1001821379673"


def QuizAfterTrialPymentPaymentDeclined():
    user_sub_end = User.objects.get(subscription_status="SECOND")

    if user_sub_end.subscription_end_date == datetime.today() - timedelta(days=1):
        quizs = Quiz.objects.get(quiz_id=4).id
        question_text = QuizQuestions.objects.filter(quiz_id_id=quizs).values('text')[0]['text']
        question_id = QuizQuestions.objects.get(quiz_id_id=quizs).id
        arr = [*[{"text": i.answer_text,
                  "callback_data": f"q{chr(quizs)}{chr(question_id)}{chr(i.answer_number)}{chr(user_sub_end.id)}"}
                 for i in QuestionAnswers.objects.filter(question_id_id=question_id)]]
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text=arr[0]['text'],
                callback_data=arr[0]['callback_data']

            )
        )
        markup.add(
            InlineKeyboardButton(
                text=arr[1]['text'],
                callback_data=arr[1]['callback_data']

            )
        )
        markup.add(
            InlineKeyboardButton(
                text=arr[2]['text'],
                callback_data=arr[2]['callback_data']

            )
        )
        markup.add(
            InlineKeyboardButton(
                text=arr[3]['text'],
                callback_data=arr[3]['callback_data']

            )
        )
        quiz(text=question_text, markup=markup, users=[user_sub_end.chat_id])


def QuizSubscriptionUsers():
    users = [i['chat_id'] for i in User.objects.filter(subscription_status="THIRD").values('chat_id')]
    for i in users:
        if User.objects.filter(chat_id=i).values('subscription_end_date')[0]['subscription_end_date'] + timedelta(
                days=1) == datetime.today():
            notification = EventsNotifications.objects.get(notifications_id=7)
            text = notification.text
            title = notification.title
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    text="🔒Закрытый клуб для подписчиков",
                    callback_data="321412"  # TODO: Вставить линк на редирект
                )
            )
            quiz(text=text, title=title, users=users, markup=markup)
        if User.objects.filter(chat_id=i).values('subscription_end_date')[0]['subscription_end_date'] + timedelta(
                days=2) == datetime.today():
            print(123)
            notification = EventsNotifications.objects.get(notifications_id=8)
            text = notification.text
            title = notification.title
            one_timeMailing(text=text, title=title, users=users)
        if User.objects.filter(chat_id=i).values('subscription_end_date')[0]['subscription_end_date'] + timedelta(
                days=3) == datetime.today():
            notification = EventsNotifications.objects.get(notifications_id=9)
            text = notification.text
            title = notification.title
            one_timeMailing(text=text, title=title, users=users)
        if User.objects.filter(chat_id=i).values('subscription_end_date')[0]['subscription_end_date'] + timedelta(
                days=4) == datetime.today():
            notification = EventsNotifications.objects.get(notifications_id=10)
            text = notification.text
            title = notification.title
            one_timeMailing(text=text, title=title, users=users)


def BanMember():
    user_sub_end_third = User.objects.get(subscription_status="THIRD")
    if user_sub_end_third.subscription_end_date == datetime.today():
        banChatMember(uId=user_sub_end_third.chat_id)

    user_sub_end_second = User.objects.get(subscription_status="SECOND")
    if user_sub_end_second.subscription_end_date == datetime.today():
        banChatMember(uId=user_sub_end_second.chat_id)
