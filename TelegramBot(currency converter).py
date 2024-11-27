from telebot import TeleBot, types

from telebot import util

from telebot import formatting

import TelegramBot_messages

import TelegramBot_currencies

from TelegramBot_commands import default_commands

from TelegramBot_currencies import default_currency_key


TOKEN = '7988214073:AAH-G_VC299CrOrLuaAl7qtOaff045AA-Yw'

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start_command(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=TelegramBot_messages.handle_start_command_text,
        parse_mode="HTML",
        reply_to_message_id=message.id,
    )


@bot.message_handler(commands=['help'])
def handle_help_command(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=TelegramBot_messages.handle_help_command_text,
        parse_mode="HTML",
        reply_to_message_id=message.id,
    )


def has_no_command_arguments(message: types.Message):
    return not util.extract_arguments(message.text)


@bot.message_handler(commands=['cvt'], func=has_no_command_arguments)
def handle_cvt_currency_no_arguments(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=TelegramBot_messages.cvt_how_to,
        parse_mode="HTML",
    )


@bot.message_handler(commands=['cvt'])
def handle_cvt_currency(message: types.Message):
    arguments = util.extract_arguments(message.text)
    amount, _, currency = arguments.partition(" ")

    if not amount.isdigit():
        error_text = formatting.format_text(
            TelegramBot_messages.invalid_argument_text,
            formatting.hcode(arguments),
            TelegramBot_messages.cvt_how_to,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=error_text,
            parse_mode="HTML",
        )
        return

    currency = currency.strip()
    default_currency = "EUR"

    user_data = bot.current_states.get_data(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    )
    if user_data and default_currency_key in user_data:
        default_currency = user_data[default_currency_key]

    currency_from, currency_to = TelegramBot_currencies.get_currencies_names(
        currency=currency,
        default_to=default_currency,
    )
    ratio = TelegramBot_currencies.get_currency_ratio(
        from_currency=currency_from,
        to_currency=currency_to,
    )
    if ratio == TelegramBot_currencies.ERROR_FETCHING_VALUE:
        bot.send_message(
            chat_id=message.chat.id,
            text=TelegramBot_messages.error_fetching_currencies_text,
        )
        return
    if ratio in {
        TelegramBot_currencies.ERROR_CURRENCY_NOT_FOUND,
        TelegramBot_currencies.ERROR_CURRENCY_INVALID,
    }:
        bad_currency = currency_from
        if ratio == TelegramBot_currencies.ERROR_CURRENCY_INVALID:
            bad_currency = currency_to
        bot.send_message(
            chat_id=message.chat.id,
            text=TelegramBot_messages.error_no_such_currency.format(
                currency=formatting.hcode(bad_currency),
            ),
            parse_mode="HTML",
        )
        return

    from_amount = int(amount)
    result_amount = from_amount * ratio
    bot.send_message(
        chat_id=message.chat.id,
        text=TelegramBot_messages.format_currency_convert_message(
            from_currency=currency_from,
            to_currency=currency_to,
            from_amount=from_amount,
            to_amount=result_amount,
        ),
        parse_mode="HTML",
    )


@bot.message_handler(commands=['usd_to_eur'])
def convert_usd_to_euro(message: types.Message):
    arguments = util.extract_arguments(message.text)
    if not arguments:
        bot.send_message(
            chat_id=message.chat.id,
            text=TelegramBot_messages.cvt_usd_to_eur_how_to,
            parse_mode="HTML",
        )
        return

    if not arguments.isdigit():
        text = formatting.format_text(
            formatting.format_text(
                TelegramBot_messages.invalid_argument_text,
                formatting.hcode(arguments),
                separator=" ",
            ),
            TelegramBot_messages.cvt_usd_to_eur_how_to,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="HTML",
        )
        return

    usd_amount = int(arguments)
    ratio = TelegramBot_currencies.get_usd_to_eur_ratio()
    eur_amount = usd_amount * ratio

    bot.send_message(
        chat_id=message.chat.id,
        text=TelegramBot_messages.format_usd_to_eur_message(
            usd_amount=usd_amount,
            eur_amount=eur_amount,
        ),
        parse_mode="HTML",
    )


@bot.message_handler(
    commands=['set_my_currency'],
    func=has_no_command_arguments,
)
def handle_no_args_to_set_my_currency(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=TelegramBot_messages.set_my_currency_help_message,
        parse_mode="HTML",
    )


@bot.message_handler(commands=['set_my_currency'])
def handle_set_my_currency(message: types.Message):
    currency = util.extract_arguments(message.text) or ""
    if not TelegramBot_currencies.is_currency_available(currency):
        bot.send_message(
            chat_id=message.chat.id,
            text=TelegramBot_messages.error_no_such_currency.format(
                currency=formatting.hcode(currency)),
            parse_mode="HTML",
        )
        return

    if bot.get_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    ) is None:
        bot.set_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            state=0,
        )

    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        **{default_currency_key: currency},
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=TelegramBot_messages.set_my_currency_success_message_text.format(
            currency=formatting.hcode(currency.upper()),
        ),
        parse_mode="HTML",
    )


if __name__ == "__main__":
    bot.enable_saving_states()
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True)
