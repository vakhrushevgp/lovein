from database import DataBase
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    MessageReactionHandler,
    filters,
)

import config
import cb


def main() -> None:
    app = Application.builder().token(config.TOKEN).build()

    app.add_handler(CommandHandler(command="start", callback=cb.start))
    app.add_handler(CommandHandler(command="day", callback=cb.day))
    app.add_handler(CommandHandler(command="month", callback=cb.month))

    app.add_handler(MessageHandler(
        filters=filters.ChatType.CHANNEL,
        callback=cb.post)
    )
    app.add_handler(MessageHandler(
        filters=filters.USER,
        callback=cb.suggestion)
    )

    app.add_handler(CallbackQueryHandler(cb.verdict))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
