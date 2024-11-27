from telebot import formatting


handle_start_command_text = "<b>I'm glad to welcome you!</b>\n Please use the <code>/help</code> command to see the full list of commands available for this bot."

handle_help_command_text = """
Hi! Available commands:
- /start - bot start 
- /help - help(this message)
- /usd_to_eur 100 - convert 100 dollars to euros
- /cvt 100 USD - converting the specified currency to euros
- /cvt 100 USD GBP - convert 100 USD to GBP
- /set_my_currency EUR - set the target currency

<b>In the near future, the capabilities of this bot will be expanded...</b>
"""

cvt_help_message = "<b>Please provide arguments for currency conversion, e.g.:</b>"

cvt_usd_to_eur_how_to = "<code>/usd_to_eur 100</code>"

cvt_how_to = formatting.format_text(
    cvt_help_message,
    "<code>/cvt 100 USD</code>",
)

invalid_argument_text = "<b>Wrong argument:</b>"
error_fetching_currencies_text = (
    "Something went wrong at the time of the request, please try again later"
)


error_no_such_currency = (
    "Unknown currency {currency}, specify an existing currency."
)


set_my_currency_help_message = formatting.format_text(
    "Please specify the selected currency. For example:",
    formatting.hcode("/set_my_currency EUR"),
)

set_my_currency_success_message_text = formatting.format_text(
    "The default currency has been successfully set:",
    "{currency}",
)


def format_currency_convert_message(
        from_currency,
        to_currency,
        from_amount,
        to_amount,
):
    return f"<code>{from_amount:,.2f}</code> <b>{from_currency.upper()}</b> is roughly <code>{to_amount:,.2f}</code> <b>{to_currency.upper()}</b>"


def format_usd_to_eur_message(usd_amount, eur_amount):
    return format_currency_convert_message(
        from_currency="USD",
        to_currency="EUR",
        from_amount=usd_amount,
        to_amount=eur_amount,
    )
