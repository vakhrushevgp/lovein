from telegram import ForceReply
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
)

import config
from database import DataBase
from datetime import datetime

BAN_LIST = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        rf"Привет {update.effective_user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=config.HI_TEXT,
    )


async def suggestion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) == config.ADMIN_CHAT_ID:
        return
    if str(update.effective_chat.id) in BAN_LIST:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ваш доступ ограничен",
        )
        return
    keyboard = [
        [
            InlineKeyboardButton("✅ Опубликовать", callback_data="V")
        ],
        [
            InlineKeyboardButton("⛔️ BAN", callback_data=f"{update.effective_chat.id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data="X")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.copy(
        chat_id=config.ADMIN_CHAT_ID,
        reply_markup=reply_markup,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Спасибо!",
    )


async def verdict(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == "V":
        await update.effective_message.copy(
            chat_id=config.CHANNEL_ID,
            reply_markup=None
        )
        await query.delete_message()
        return
    if query.data == "X":
        await query.edit_message_reply_markup()
        return
    if query.data in BAN_LIST:
        BAN_LIST.remove(query.data)
        await query.edit_message_reply_markup()
    else:
        BAN_LIST.add(query.data)
        btn = InlineKeyboardButton("🙈 Разбанить", callback_data=query.data)
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([[btn]])
        )


async def post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != config.CHANNEL_ID:
        return
    mes = update.effective_message
    db = DataBase(config.DATA_FILE)
    db.add(
        post_id=mes.message_id,
        info=[mes.date.month, mes.date.day, 0]
    )


async def reactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) != config.CHANNEL_ID:
        return
    db = DataBase(config.DATA_FILE)
    upd = update.message_reaction_count
    post_id = upd.message_id
    count = 0
    for emoji in upd.reactions:
        count += emoji.total_count
    db.update(post_id, count)


async def day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    date = datetime.now().strftime("%d %B")
    db = DataBase(config.DATA_FILE)
    post_id = db.day()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Лучший пост за сегодня ({date})\nhttps://t.me/jerkdalcsx/{post_id}",
    )


async def month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    month = datetime.now().strftime("%B")
    db = DataBase(config.DATA_FILE)
    post_id = db.month()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Лучший пост за месяц ({month})\nhttps://t.me/jerkdalcsx/{post_id}",
    )
