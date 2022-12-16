from telebot import *
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InlineQuery,
)
from variables import *
from api import *
from chnnaelAccess import *

bot = TeleBot(token)
print("bot is running...")

'''
________________________________________________________________________________________________________________________
Inline keyboards
________________________________________________________________________________________________________________________
'''
subscribeUrlKb = InlineKeyboardMarkup(row_width=1)
subscribeUrlKb.add(InlineKeyboardButton(text="💳 Оформить подписку", url=subscribeLink))

'''
________________________________________________________________________________________________________________________
Keyboards
________________________________________________________________________________________________________________________
'''
mainKb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mainKb.add(KeyboardButton("Статус подписки"))
mainKb.add(KeyboardButton("База знаний"))
mainKb.add(KeyboardButton("Закрытый чат"))

'''
________________________________________________________________________________________________________________________
Local functions
________________________________________________________________________________________________________________________
'''

months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня",
          "Июля", "Августа", "Сентября", "Октября", "Ноябля", "Декабря"]


def statusMessage(uId: int):
    markup = InlineKeyboardMarkup(row_width=1)
    user = getUser(uId)

    if user.subscriptionStatus == "FIRST":
        messageText = "Ты еще не оформлял бесплатный триал. 🤩 Хочешь получить 3 дня доступа бесплатно?"
        markup.add(InlineKeyboardButton(text="✅ Подписаться", url=subscribeLink))
    elif user.subscriptionStatus == "SECOND":
        if user.subscriptionEndDate > datetime.now():
            messageText = f"Твой бесплатный триал завершается ➡ {user.subscriptionEndDate.day} " \
                          f"{months[user.subscriptionEndDate.month-1]} {user.subscriptionEndDate.year} года"
            markup.add(InlineKeyboardButton(text="✅ Подписаться", url=subscribeLink))
        else:
            messageText = "😎 Ты уже прошел бесплатный триал. Чтобы получать прогнозы, подпишись"
            markup.add(InlineKeyboardButton(text="✅ Подписаться", url=subscribeLink))
            markup.add(InlineKeyboardButton(text="✍ Остались вопросы", url=subscribeLink))
    elif user.subscriptionStatus == "THIRD":
        if user.subscriptionEndDate > datetime.now():
            messageText = f"Твой платная подписка действует до ➡ {user.subscriptionEndDate.day} " \
                          f"{months[user.subscriptionEndDate.month-1]} {user.subscriptionEndDate.year} года"
        else:
            messageText = f"Твой платная подписка акончилась ➡ {user.subscriptionEndDate.day} " \
                          f"{months[user.subscriptionEndDate.month-1]} {user.subscriptionEndDate.year} года"
            markup.add(InlineKeyboardButton(text="Продлить подписку", url=subscribeLink))

    else:
        messageText = f"Произошла какая-то ошибка"
        markup.add(InlineKeyboardButton(text="Обратится к администратору", url=adminLink))

    return messageText, markup


'''
________________________________________________________________________________________________________________________
Commands
________________________________________________________________________________________________________________________
'''


# @bot.message_handler(commands=['start'])
# def send_hi(message: Message):
#     print(message.chat.id, " - ", message.chat.first_name, " send /start")
#     bot.send_message(message.chat.id, "Привет ✌️ ")


def onRegControl(message: Message):
    uId = message.chat.id
    user = getUser(uId)
    joinLink = generateJoinLink(message.from_user.username, uId)
    websiteUrlKb = InlineKeyboardMarkup(row_width=1)
    websiteUrlKb.add(InlineKeyboardButton(text="🔗Связать*", url=joinLink))
    if user.siteId is None:
        bot.send_message(uId,
                         "🔗 Чтобы привязать свой телеграм к аккаунту на DataLouna.ru, просто нажми на кнопку “Связать” под этим сообщением."
                         ""
                         "Привязка делается один раз.",
                         reply_markup=websiteUrlKb)
        bot.register_next_step_handler(message, onRegControl)
    return


@bot.message_handler(commands=['start'])
def send_hi(message: Message):
    # print(message.chat.id, " - ", message.chat.first_name, " send /start")
    messageText = getMessageTexts(4)
    if messageText is None:
        bot.send_message(message.chat.id, '''Произошла какая-то ошибка, обратитесь к администратору.''')
    bot.send_message(message.chat.id, text=messageText, reply_markup=mainKb, parse_mode="Markdown")
    if getUser(message.chat.id) is None:
        createUser(message.chat.id)
    onRegControl(message)


@bot.message_handler(commands=['faq'])
def knowledgeBase(message: types.Message):
    user = getUser(message.chat.id)
    if user.subscriptionEndDate is None:
        bot.send_message(message.chat.id, text="Пока не могу показать тебе эту информацию.\n"
                                               "Сначала оформи подписку.", reply_markup=subscribeUrlKb)
        return
    if user.subscriptionEndDate < datetime.now():
        bot.send_message(message.chat.id,
                         text="К сожалению твоя подписка уже закончилась и я больше не могу показать тебе эту информацию.",
                         reply_markup=subscribeUrlKb)
        return

    markup = InlineKeyboardMarkup()
    root = getArticle()
    # ---------------------------------------------------------------
    if root is None:
        print("__ ", message.chat.id)
        bot.send_message(message.from_user.id, "Error!!!")
        return
    # ---------------------------------------------------------------
    for i in root.childList:
        # ---------------------------------------------------------------
        if i is None:
            bot.send_message(message.from_user.id, "Error!!!")
            return
        markup.add(
            InlineKeyboardButton(
                text=i.title,
                callback_data="a" + chr(root.id)
                              + chr(i.id),
            )
        )  # parentId

    markup.add(
        InlineKeyboardButton(
            text="Поиск",
            switch_inline_query_current_chat=""
        )
    )
    bot.send_message(message.from_user.id, root.title + "\n\nКатегории", reply_markup=markup)


'''
________________________________________________________________________________________________________________________
Inline buttons
________________________________________________________________________________________________________________________
'''


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call: CallbackQuery):
#     markup = InlineKeyboardMarkup()
#     cbdata = call.data
#     if cbdata[0] == 'unseen':
#         bot.delete_message(call.message.chat.id, call.message.message_id)
# elif cbdata[0] == 'a':


@bot.callback_query_handler(func=lambda call: call.data[0] == 'a')
def articleCallback(call: CallbackQuery):
    user = getUser(call.message.chat.id)
    if user.subscriptionEndDate is None:
        bot.send_message(call.message.chat.id,
                         text="Не понимаю как ты сюда попал. Должно быть случилась какая-то ошибка.\n"
                              "Сначала оформи подписку.", reply_markup=subscribeUrlKb)
        return
    if user.subscriptionEndDate < datetime.now():
        bot.send_message(call.message.chat.id,
                         text="К сожалению твоя подписка уже закончилась и я больше не могу показать тебе эту информацию.",
                         reply_markup=subscribeUrlKb)
        return

    markup = InlineKeyboardMarkup()
    cbdata = call.data[1:]
    article = getArticle(ord(cbdata[-1]))
    if len(cbdata) + 3 == 40:
        cbdata = cbdata[3:]
    # ---------------------------------------------------------------
    if article is None:
        print("__ ", call.message.chat.id)
        bot.send_message(call.from_user.id, "Error!!!")
        return
    bot.delete_message(call.message.chat.id, call.message.id)
    for i in article.childList:
        # ---------------------------------------------------------------
        if i is None:
            bot.send_message(call.message.chat.id, "Error!!!")
            return
        markup.add(
            InlineKeyboardButton(
                text=i.title,
                callback_data="a" + cbdata
                              + chr(i.id),
            )
        )  # parentId

    # markup.add(
    #             InlineKeyboardButton(
    #                 text="Назад",
    #                 callback_data="a" + cbdata[:-1]
    #             )
    #         )
    # markup.add(
    #             InlineKeyboardButton(
    #                 text="На главную",
    #                 callback_data="a" + chr(getArticle().id)
    #             )
    #         )
    if len(cbdata) == 2 and ord(cbdata[0]) != getArticle().id:
        markup.add(
            InlineKeyboardButton(
                text="На главную",
                callback_data="a" + chr(getArticle().id)
            )
        )
    elif len(cbdata) >= 2:
        markup.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="a" + cbdata[:-1]
            )
        )  # parentId))
        markup.add(
            InlineKeyboardButton(
                text="На главную",
                callback_data="a" + chr(getArticle().id)
            )
        )
    if article.id == getArticle().id:
        markup.add(
            InlineKeyboardButton(
                text="Поиск",
                switch_inline_query_current_chat=""
            )
        )
    # print(article.photoPath)
    messageText = f'*{article.title}*\n\n{article.text}'
    img = getPhoto(article.photoPath)
    # print(img)
    if img:
        bot.send_photo(
            call.message.chat.id,
            img,
            caption=messageText,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            call.message.chat.id,
            messageText,
            reply_markup=markup,
            parse_mode="Markdown",
        )


@bot.callback_query_handler(func=lambda call: call.data[0] == 'q')
def quizResponsesCatcher(call: CallbackQuery):
    codedAnswere = call.data + chr(call.message.chat.id)
    sendQuizAnswer(codedAnswere)


'''
________________________________________________________________________________________________________________________
Keyboard buttons
________________________________________________________________________________________________________________________
'''


@bot.message_handler(content_types=['text'])
def mainKeyboard(message: Message):
    if message.text == "Статус подписки":
        user = getUser(message.chat.id)
        messageText, kbMarkup = statusMessage(user.chatId)
        bot.send_message(message.chat.id, text=messageText, reply_markup=kbMarkup)
    elif message.text == "База знаний":
        user = getUser(message.chat.id)
        if user.subscriptionEndDate is None:
            bot.send_message(message.chat.id,
                             text="Пока не могу показать тебе эту информацию.\n"
                                  "Сначала оформи подписку.", reply_markup=subscribeUrlKb)
        elif user.subscriptionEndDate < datetime.now():
            bot.send_message(message.chat.id,
                             text="К сожалению твоя подписка уже закончилась и я больше не могу показать тебе эту "
                                  "информацию.",
                             reply_markup=subscribeUrlKb)
        else:
            knowledgeBase(message)

    elif message.text == "Закрытый чат":
        user = getUser(message.chat.id)
        if user.subscriptionEndDate is None:
            bot.send_message(message.chat.id,
                             text="Вы пока не оформили подписку поэтому не могу предоставить вам доступ.",
                             reply_markup=subscribeUrlKb)
        elif user.subscriptionEndDate < datetime.now():
            bot.send_message(message.chat.id,
                             text="К сожалению твоя подписка уже закончилась и твой доступ в закрытый чат "
                                  "временно закрыт.",
                             reply_markup=subscribeUrlKb)
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text="Попасть в закрытый чат 😎", url=createInvteLink()))
            bot.send_message(message.chat.id, text="Вот тебе ссылка для входа в закрытый чат", reply_markup=markup)


'''
________________________________________________________________________________________________________________________
Inline mode
________________________________________________________________________________________________________________________
'''


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inlineMode(data: InlineQuery):
    # print(data)
    # print(data.query)
    articles = getArticlesByKeyWord(data.query)
    # print(articles)
    if articles == None:
        return
    inlineQuery = []
    cnt = 1
    for article in articles:
        inlineQuery.append(
            types.InlineQueryResultArticle(
                id=str(cnt),
                title=article.title,
                input_message_content=articleToMessage(article),
                description=article.text[:30] + "...",
            )
        )
        cnt += 1
    bot.answer_inline_query(str(data.id), inlineQuery)


'''
________________________________________________________________________________________________________________________
Channel access
________________________________________________________________________________________________________________________
'''


@bot.chat_join_request_handler()
def joinChannelReques(request: types.ChatJoinRequest):
    # res = getAccess(request.chat.id)
    # print("avavavvavavvavavavva")
    # bot.approve_chat_join_request(chat_id=-1001821379673, user_id=354640082)
    uid = request.from_user.id
    res = getAccess(uid)
    print("chatJoinRequest")
    print(request)
    if res:

        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="Перейти в канал", url=createInvteLink()))
        bot.send_message(uid, text="Вы успешно добавлены в канал.", )
    else:
        bot.send_message(uid, text="Вам отказано в доступе в канал. Оформите или продлите подкиску.",
                         reply_markup=subscribeUrlKb)


'''
________________________________________________________________________________________________________________________
Main access
________________________________________________________________________________________________________________________
'''

'''
________________________________________________________________________________________________________________________
Bot polling
________________________________________________________________________________________________________________________
'''

bot.infinity_polling()
