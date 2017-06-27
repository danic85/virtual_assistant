import datetime
import calendar


def period_from_datetime(dt):
    now = datetime.datetime.now()
    delta = dt - datetime.datetime(now.year, now.month, now.day, 0, 0)
    output = []
    days = delta.days
    if days >= 7 or days < 0:
        if days >= 14 or days < 0:
            output.append('a')
        else:
            output.append('next')
    if days > 0 or days < 0:
        output.append(calendar.day_name[dt.weekday()])

    period = None
    if dt.hour < 7:
        period = 'early morning'
    elif dt.hour < 12:
        period = 'morning'
    elif dt.hour < 15:
        period = 'midday'
    elif dt.hour < 18:
        period = 'afternoon'
    elif dt.hour < 21:
        period = 'evening'
    else:
        period = 'night'
    if days == 0:
        if period == 'night':
            period = 'tonight'
        elif period == 'early morning':
            period = 'early this morning'
        else:
            output.append('this')
    output.append(period)
    return ' '.join(output)


def datetime_from_time(hour, minute):
    dt = datetime.datetime.now()
    if dt.hour > hour or (dt.hour == hour and dt.minute > minute):  # don't fire straight away, make it for tomorrow if earlier than now
        dt = datetime.datetime.now() + datetime.timedelta(days=1)
    return datetime.datetime(dt.year, dt.month, dt.day, hour, minute, 0)


def datetime_from_time_of_day(context, period):
    dt = datetime.datetime.now()
    if context == 'tomorrow':
        dt = dt + datetime.timedelta(days=1)

    periods = {'morning': 7, 'lunch': 12, 'lunchtime': 12, 'afternoon': 15, 'evening': 19, 'night': 22}
    if period in periods.keys():
        time = periods[period]
    else:
        time = 0

    dt = datetime.datetime(dt.year, dt.month, dt.day, time, 0)

    return dt


def datetime_from_hours(hours):
    return datetime.datetime.now() + datetime.timedelta(hours=int(hours))
