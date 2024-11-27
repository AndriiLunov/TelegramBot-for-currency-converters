from telebot.types import BotCommand

default_commands = [
    BotCommand("start", "bot start"),
    BotCommand("help", "help"),
    BotCommand("usd_to_eur", "convert dollars to euros"),
    BotCommand("cvt", "convert"),
    BotCommand("/set_my_currency", "set the target currency")
]
