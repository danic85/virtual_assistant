import datetime
import calendar

def datetime_period_from_datetime(dt):
    now = datetime.datetime.now()
    delta = dt - datetime.datetime(now.year, now.month, now.day, 0, 0)
    output = []
    days = delta.days
    print(days)
    if days >= 7:
        if days >= 14:
            output.append('a')
        else:
            output.append('next')
    if days > 0:
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

print(datetime_period_from_datetime(datetime.datetime(2017,5,29,3,0)))
print(datetime_period_from_datetime(datetime.datetime(2017,6,29,23,0)))
print(datetime_period_from_datetime(datetime.datetime(2017,7,1,12,0)))
print(datetime_period_from_datetime(datetime.datetime(2017,6,29,14,0)))
print(datetime_period_from_datetime(datetime.datetime(2017,6,29,21,0)))
print('THE NEXT 20 DAYS:')
for i in range(0,20):
    print(datetime_period_from_datetime(datetime.datetime(2017,6,27,23,0)+datetime.timedelta(days=i)))
print('THE FULL DAY')
for i in range(0,24):
    print(str(i) + ': ' + datetime_period_from_datetime(datetime.datetime(2017,6,27,i,0)))
