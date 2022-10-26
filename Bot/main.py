from telebot import *
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InlineQuery,
)
from LounaAdmin.variables import *
from api import *

bot = TeleBot(token)
print("bot is running...")

'''
________________________________________________________________________________________________________________________
Commands
________________________________________________________________________________________________________________________
'''


@bot.message_handler(commands=['start'])
def send_hi(message: Message):
    print(message.chat.id, " - ", message.chat.first_name, " send /start")
    bot.send_message(message.chat.id, "Привет ✌️ ")


@bot.message_handler(commands=['faq'])
def send_category(message: types.Message):
    markup = InlineKeyboardMarkup()
    root = getChildren()[0]
    # ---------------------------------------------------------------
    if root is None:
        print("__ ", message.chat.id)
        bot.send_message(message.from_user.id, "Error!!!")
        return
    children = getChildren(root.id)
    # ---------------------------------------------------------------
    if children is None:
        print("__ ", message.chat.id)
        bot.send_message(message.from_user.id, "Error!!!")
        return
    for i in children:
        # ---------------------------------------------------------------
        if i is None:
            bot.send_message(message.from_user.id, "Error!!!")
            return
        markup.add(
            InlineKeyboardButton(
                text=i.name,
                callback_data="c\0"
                + str(int(i.final))
                + "\0"  # type and final
                + str(i.id)
                + "\0"  # id
                + str(i.parentId),
            )
        )  # parentId
    bot.send_message(message.from_user.id, root.name + "\n\nКатегории", reply_markup=markup)


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


@bot.callback_query_handler(func=lambda call: call.data.split('\0')[0] == 'c')
def categoryCallback(call: CallbackQuery):
    """

    :param call:
    :return:
    """
    markup = InlineKeyboardMarkup()
    cbdata = call.data
    cbdata = cbdata.split('\0')
    if int(cbdata[1]):
        articles = getArticlesByNode(int(cbdata[2]))
        # ---------------------------------------------------------------
        if articles is None:
            print("__ ", call.message.chat.id)
            bot.send_message(call.from_user.id, "Error!!!")
            return
        for article in articles:
            # ---------------------------------------------------------------
            if article is None:
                bot.send_message(call.from_user.id, "Error!!!")
                return
            markup.add(
                InlineKeyboardButton(
                    text=article.title,
                    callback_data="a\0" + str(article.id) + "\0" + cbdata[2],  # id
                )
            )  # parentId
        node = getNode(int(cbdata[2]))
        parentId = node.parentId
        messageText = node.name
        node = getNode(parentId)
        markup.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="c\0"
                + str(int(node.final))
                + "\0"  # type and final
                + str(node.id)
                + "\0"  # id
                + str(node.parentId),
            )
        )  # parentId
        while True:
            if parentId is None:
                break
            node = getNode(parentId)
            parentId = node.parentId
            messageText = f'{node.name} → {messageText}'
        messageText = messageText + "\n\nСтатьи:"

        if len(cbdata) == 5 and int(cbdata[-1]):
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(
                chat_id=call.message.chat.id,
                text=messageText,
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=messageText,
            reply_markup=markup,
        )
    else:
        categories = getChildren(int(cbdata[2]))
        if categories is None:
            print("__ ", call.from_user.id)
            bot.send_message(call.from_user.id, "Error!!!")
            return
        for category in categories:
            # ---------------------------------------------------------------
            if category is None:
                bot.send_message(call.from_user.id, "Error!!!")
                return
            markup.add(
                InlineKeyboardButton(
                    text=category.name,
                    callback_data="c\0"
                    + str(int(category.final))
                    + "\0"  # type and final
                    + str(category.id)
                    + "\0"  # id
                    + str(category.parentId),
                )
            )  # parentId
        node = getNode(int(cbdata[2]))
        parentId = node.parentId
        messageText = node.name
        node = getNode(parentId)
        if parentId != None:
            markup.add(
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="c\0"
                    + str(int(node.final))
                    + "\0"  # type and final
                    + str(node.id)
                    + "\0"  # id
                    + str(node.parentId),
                )
            )  # parentId
        while True:
            if parentId is None:
                break
            node = getNode(parentId)
            parentId = node.parentId
            messageText = f'{node.name} → {messageText}'

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=messageText + "\n\nКатегории:",
            reply_markup=markup,
        )


@bot.callback_query_handler(func=lambda call: call.data.split('\0')[0] == 'a')
def articleCallback(call: CallbackQuery):
    markup = InlineKeyboardMarkup()
    cbdata = call.data
    cbdata = cbdata.split('\0')
    article = getArticle(int(cbdata[1]))
    # ---------------------------------------------------------------
    if article is None:
        print("__ ", call.message.chat.id)
        bot.send_message(call.from_user.id, "Error!!!")
        return
    bot.delete_message(call.message.chat.id, call.message.id)
    node = getNode(int(cbdata[2]))
    # ---------------------------------------------------------------
    if node is None:
        print("__ ", call.message.chat.id)
        bot.send_message(call.from_user.id, "Error!!!")
        return
    markup.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data="c\0"
            + str(int(node.final))
            + "\0"  # type and final
            + str(node.id)
            + "\0"  # id
            + str(node.parentId)
            + "\0"  # delete
            + str(int(True)),
        )
    )  # parentId))
    messageText = f'*{article.title}*\n\n{article.text}'
    img = getPhoto(article.photoPath)
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
    bot.answer_inline_query(data.id, inlineQuery)


bot.infinity_polling()
