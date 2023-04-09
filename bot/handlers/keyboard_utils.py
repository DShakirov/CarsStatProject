from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.handlers import manage_data as md
from bot.handlers import static_text as st


def make_btn_keyboard():
    buttons = [
        [
            InlineKeyboardButton(st.go_back, callback_data=f'{md.BUTTON_BACK_IN_PLACE}'),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_start_command():
    buttons = [
        [
            InlineKeyboardButton(st.btn1, callback_data=f'{md.CHP_LTE_500}'),
        ],
        [
            InlineKeyboardButton(st.btn2, callback_data=f'{md.BTN_2}'),
            InlineKeyboardButton(st.btn3, callback_data=f'{md.BTN_3}'),
        ],
        [
            InlineKeyboardButton(st.btn4, callback_data=f'{md.BTN_4}'),
        ],
                [
            InlineKeyboardButton(st.btn5, callback_data=f'{md.BTN_5}'),
            InlineKeyboardButton(st.btn6, callback_data=f'{md.BTN_6}'),
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def keyboard_confirm_decline_broadcasting():
    buttons = [[
        InlineKeyboardButton(st.confirm_broadcast, callback_data=f'{md.CONFIRM_DECLINE_BROADCAST}{md.CONFIRM_BROADCAST}'),
        InlineKeyboardButton(st.decline_broadcast, callback_data=f'{md.CONFIRM_DECLINE_BROADCAST}{md.DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)