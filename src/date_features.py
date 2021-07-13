from datetime import (
    datetime,
    date,
)
from dateutil.relativedelta import (
    relativedelta,
)

from pytz import (
    timezone,
    UTC,
)


def get_current_date():
    """
    Получаем текущую дату
    :return: datetime - текущая дата
    """
    return datetime.now()


def get_expire_date(months):
    """
    Возарщает дату дедлайна (истечения срока действия)
    :param months: int - через сколько месяцев дедлайн
    :return: datetime - дата дедлайна
    """
    return datetime.now() + relativedelta(months=+months)


def get_maximum_date():
    """
    Возвращает максимально возможную дату
    :return: datetime - максимально возможная дата
    """
    return date.max


def get_moscow_time_week_day(ts):
    server_time = datetime.fromtimestamp(ts)
    moscow_time = server_time.astimezone(timezone('Europe/Moscow'))
    moscow_day = moscow_time.today().weekday()
    result_time = UTC.localize(datetime.strptime(
        f'{moscow_time.hour}:{moscow_time.minute}:{moscow_time.second}', '%H:%M:%S'))

    return result_time, moscow_day


def check_message_day_time(curr_time, day):
    weekend = [4, 5]
    f = '%H:%M:%S'
    result = False
    late_time = UTC.localize(datetime.strptime('17:30:00', f))
    too_late_time = UTC.localize(datetime.strptime('23:59:59', f))
    early_time = UTC.localize(datetime.strptime('08:00:00', f))
    if (late_time < curr_time < too_late_time or curr_time < early_time) and day not in weekend:
        result = True
    elif day in weekend:
        result = True
    return result

