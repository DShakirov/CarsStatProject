import datetime
import logging
import telegram
import time
from django.utils import timezone

from bot.handlers import commands
from bot.handlers import static_text as st
from bot.handlers import manage_data as md
from bot.handlers import keyboard_utils as kb
from bot.handlers.utils import handler_logging
from bot.models import User
from bot.tasks import broadcast_message
from bot.utils import convert_2_user_time, extract_user_data_from_update, get_chat_id
from carsstat.models import Car

logger = logging.getLogger('default')


@handler_logging()
def show_cheap_lte_500_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)
    markup = kb.make_btn_keyboard()
    cars = Car.objects.raw(
        'SELECT car.sell_id, car.created_at, car.year, car.link, car.price, mark.name AS markname, carmodel.name AS carmodel_name '
        'FROM carsstat_car AS car '
        'JOIN carsstat_mark AS mark ON car.mark_id = mark.id JOIN carsstat_carmodel AS carmodel ON car.car_model_id = carmodel.id '
        'WHERE(car.price <= 500000) AND(car.low_price = True) ORDER BY car.created_at'
         )[:25]
    for car in cars:
        time.sleep(1)
        msg = f'{car.markname} {car.carmodel_name} {car.year} {car.price}\n {car.link}'

        context.bot.send_message(
            text=msg,
            chat_id=user_id,
            )

    context.bot.send_message(
        text='Больше автомобилей на сайте.',
        chat_id=user_id,
        reply_markup=markup,
    )

def show_cheap_lte_1mln_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)
    markup = kb.make_btn_keyboard()
    cars = Car.objects.raw(
        'SELECT car.sell_id, car.created_at, car.year, car.link, car.price, mark.name AS markname, carmodel.name AS carmodel_name '
        'FROM carsstat_car AS car '
        'JOIN carsstat_mark AS mark ON car.mark_id = mark.id JOIN carsstat_carmodel AS carmodel ON car.car_model_id = carmodel.id '
        'WHERE(car.price >= 500000 AND car.price <= 1000000 ) AND(car.low_price = True) ORDER BY car.created_at'
         )[:25]
    for car in cars:
        time.sleep(1)
        msg = f'{car.markname} {car.carmodel_name} {car.year} {car.price}\n {car.link}'

        context.bot.send_message(
            text=msg,
            chat_id=user_id,
            )

    context.bot.send_message(
        text='Больше автомобилей на сайте.',
        chat_id=user_id,
        reply_markup=markup,)


@handler_logging()
def show_cheap_gte_1mln_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)
    markup = kb.make_btn_keyboard()
    cars = Car.objects.raw(
        'SELECT car.sell_id, car.created_at, car.year, car.link, car.price, mark.name AS markname, carmodel.name AS carmodel_name '
        'FROM carsstat_car AS car '
        'JOIN carsstat_mark AS mark ON car.mark_id = mark.id JOIN carsstat_carmodel AS carmodel ON car.car_model_id = carmodel.id '
        'WHERE(car.price >= 1000000) AND(car.low_price = True) ORDER BY car.created_at'
         )[:25]
    for car in cars:
        time.sleep(1)
        msg = f'{car.markname} {car.carmodel_name} {car.year} {car.price}\n {car.link}'

        context.bot.send_message(
            text=msg,
            chat_id=user_id,
            )

    context.bot.send_message(
        text='Больше автомобилей на сайте.',
        chat_id=user_id,
        reply_markup=markup,)

@handler_logging()
def show_expensive_lte_500_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)
    markup = kb.make_btn_keyboard()
    cars = Car.objects.raw(
        'SELECT car.sell_id, car.created_at, car.year, car.link, car.price, mark.name AS markname, carmodel.name AS carmodel_name '
        'FROM carsstat_car AS car '
        'JOIN carsstat_mark AS mark ON car.mark_id = mark.id JOIN carsstat_carmodel AS carmodel ON car.car_model_id = carmodel.id '
        'WHERE(car.price <= 500000) AND(car.high_price = True) ORDER BY car.created_at'
         )[:25]
    for car in cars:
        time.sleep(1)
        msg = f'{car.markname} {car.carmodel_name} {car.year} {car.price}\n {car.link}'

        context.bot.send_message(
            text=msg,
            chat_id=user_id,
            )

    context.bot.send_message(
        text='Больше автомобилей на сайте.',
        chat_id=user_id,
        reply_markup=markup,
    )

def show_expensive_lte_1mln_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)
    markup = kb.make_btn_keyboard()
    cars = Car.objects.raw(
        'SELECT car.sell_id, car.created_at, car.year, car.link, car.price, mark.name AS markname, carmodel.name AS carmodel_name '
        'FROM carsstat_car AS car '
        'JOIN carsstat_mark AS mark ON car.mark_id = mark.id JOIN carsstat_carmodel AS carmodel ON car.car_model_id = carmodel.id '
        'WHERE(car.price >= 500000 AND car.price <= 1000000 ) AND(car.high_price = True) ORDER BY car.created_at'
         )[:25]
    for car in cars:
        time.sleep(1)
        msg = f'{car.markname} {car.carmodel_name} {car.year} {car.price}\n {car.link}'

        context.bot.send_message(
            text=msg,
            chat_id=user_id,
            )

    context.bot.send_message(
        text='Больше автомобилей на сайте.',
        chat_id=user_id,
        reply_markup=markup,)

@handler_logging()
def show_expensive_gte_1mln_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)
    markup = kb.make_btn_keyboard()
    cars = Car.objects.raw(
        'SELECT car.sell_id, car.created_at, car.year, car.link, car.price, mark.name AS markname, carmodel.name AS carmodel_name '
        'FROM carsstat_car AS car '
        'JOIN carsstat_mark AS mark ON car.mark_id = mark.id JOIN carsstat_carmodel AS carmodel ON car.car_model_id = carmodel.id '
        'WHERE(car.price >= 1000000) AND(car.low_price = True) ORDER BY car.created_at'
         )[:25]
    for car in cars:
        time.sleep(1)
        msg = f'{car.markname} {car.carmodel_name} {car.year} {car.price}\n {car.link}'

        context.bot.send_message(
            text=msg,
            chat_id=user_id,
            )

    context.bot.send_message(
        text='Больше автомобилей на сайте.',
        chat_id=user_id,
        reply_markup=markup,)

@handler_logging()
def back_to_main_menu_handler(update, context):  # callback_data: BUTTON_BACK_IN_PLACE variable from manage_data.py
    user, created = User.get_user_and_created(update, context)

    payload = context.args[0] if context.args else user.deep_link  # if empty payload, check what was stored in DB
    text = st.welcome

    user_id = extract_user_data_from_update(update)['user_id']
    context.bot.edit_message_text(
        chat_id=user_id,
        text=text,
        message_id=update.callback_query.message.message_id,
        reply_markup=kb.make_keyboard_for_start_command(),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@handler_logging()
def secret_level(update, context): #callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
           "*Users*: {user_count}\n" \
           "*24h active*: {active_24}".format(
            user_count=User.objects.count(),
            active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def broadcast_decision_handler(update, context): #callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(md.CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities = update.callback_query.message.entities
    text = update.callback_query.message.text
    if broadcast_decision == md.CONFIRM_BROADCAST:
        admin_text = st.msg_sent,
        user_ids = list(User.objects.all().values_list('user_id', flat=True))
        broadcast_message.delay(user_ids=user_ids, message=text, entities=entities_for_celery)
    else:
        admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == md.CONFIRM_BROADCAST else entities
    )
