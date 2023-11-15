from datetime import date, timedelta, datetime

dob = datetime(year=1980, month=11, day=17)
# print(dob.month)
# print(dob.day)

today = date.today()
# print(today.month)
# print(today.day)
interval = 48

interval_target_date = timedelta(days=interval)
# print(today + interval_target_date)

print((datetime.now() + interval_target_date).year)
print((datetime.now() + interval_target_date).month)
print((datetime.now() + interval_target_date).day)
