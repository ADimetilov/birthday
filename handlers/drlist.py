from datetime import datetime,timedelta

def return_month():
    now = datetime.now()                     
    add_month = timedelta(31)
    month = now + add_month  
    return month.strftime("%d.%m")

def return_week():
    now = datetime.now()
    add_wick = timedelta(weeks=1)
    week = now + add_wick
    return week.strftime("%d.%m")

def return_day():
    now = datetime.now()
    add_day = timedelta(days=1)
    day = now+add_day
    return day.strftime("%d.%m")

def days_until_birthday(birthday_str: str) -> int:
    today = datetime.today()
    birth_day, birth_month = map(int, birthday_str.split('.'))
    birthday_this_year = datetime(today.year, birth_month, birth_day)
    
    if birthday_this_year < today:
        birthday_this_year = datetime(today.year + 1, birth_month, birth_day)
    
    return (birthday_this_year - today).days
