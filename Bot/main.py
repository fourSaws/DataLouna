from telebot import *
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
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
websiteUrlKb = InlineKeyboardMarkup(row_width=1)
websiteUrlKb.add(InlineKeyboardButton(text="🔗Связать*", url=websiteLink))
subscribeUrlKb = InlineKeyboardMarkup(row_width=1)
subscribeUrlKb.add(InlineKeyboardButton(text="💳 Оформить подписку", url=subscribeLink))

'''
________________________________________________________________________________________________________________________
Commands
________________________________________________________________________________________________________________________
'''

# @bot.message_handler(commands=['start'])
# def send_hi(message: Message):
#     print(message.chat.id, " - ", message.chat.first_name, " send /start")
#     bot.send_message(message.chat.id, "Привет ✌️ ")



def onRegControl(message):
    uId = message.chat.id
    user = getUser(uId)
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
    print(message.chat.id, " - ", message.chat.first_name, " send /start")
    bot.send_message(message.chat.id, '''👋 Привет, я — твой персональный помощник в работе с нашим сервисом DataLouna.ru. Вот, что ждет тебя внутри:🧠 Объясним, как начать зарабатывать с DataLouna
    
💲 Управление банком

💰 Как не растерять все деньги и преумножить их

👀 Уникальные фишки — в боте раньше, чем на сайте

🎁 Ежемесячные конкурсы

🤔 Ответы на все твои вопросы

🤝 Информация о твоей подписке😎 Закрытый клуб для подписчиков, в котором сидят создатели DataLouna''')
    if getUser(message.chat.id) is None:
        createUser(message.chat.id)
    onRegControl(message)



@bot.message_handler(commands=['faq'])
def send_category(message: types.Message):
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
    markup = InlineKeyboardMarkup()
    cbdata = call.data[1:]
    article = getArticle(ord(cbdata[-1]))
    if len(cbdata) + 1 == 40:
        cbdata = cbdata[1:]
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
    if len(cbdata) == 2 and ord(cbdata[0]) != getArticle().id:
        markup.add(
            InlineKeyboardButton(
                text="На главную",
                callback_data="a"+chr(getArticle().id)
            )
        )
    elif len(cbdata) >= 2:
        markup.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="a"+cbdata[:-1]
            )
        )  # parentId))
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

'''
________________________________________________________________________________________________________________________
Inline mode
________________________________________________________________________________________________________________________
'''


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inlineMode(data: InlineQuery):
    print(data)
    print(data.query)
    articles = getArticlesByKeyWord(data.query)
    print(articles)
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
    res = True
    if res:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton(text="Перейти в канал", url=createInvteLink()))
        bot.send_message(request.chat.id, text="Вы успешно добавлены в канал.", )
    else:
        bot.send_message(request.chat.id, text="Вам отказано в доступе в канал. Оформите или продлите подкиску.", reply_markup=subscribeUrlKb)


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


