from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.drlist import days_until_birthday
def get_inline_menu(ln:str):
    builder = InlineKeyboardBuilder()
    if ln == "Ru":
        builder.row(InlineKeyboardButton(text="Добавить день рождения🎂",callback_data="birthday_add"),InlineKeyboardButton(text="Список дней рождения🎁",callback_data="birthday_list"),width=1)
        builder.button(text="Настройки(Settings)⚙️",callback_data="setting")
        builder.adjust(1)
        builder.button(text="Наш телеграм-канал🗞", url = "https://t.me/ubshushik")
    else:
        builder.row(InlineKeyboardButton(text="Add a birthday🎂",callback_data="birthday_add"),InlineKeyboardButton(text="List of birthdays🎁",callback_data="birthday_list"),width=1)
        builder.button(text="Settings(Настройки)⚙️",callback_data="setting")
        builder.adjust(1)
        builder.button(text="Our telegram channel🗞", url = "https://t.me/ubshushik")
    return builder.as_markup()

def notifi_change(ln:str):
    builder = InlineKeyboardBuilder()
    if ln == "Ru":
        builder.button(text = "Включить🔔",callback_data="inter_on")
        builder.button(text = "Выключить🔕",callback_data="inter_off")
        builder.button(text="Вернуться в меню⬅️",callback_data="menu")
    else:
        builder.button(text = "Turn on🔔",callback_data="inter_on")
        builder.button(text = "Turn off🔕",callback_data="inter_off")
        builder.button(text="Go back to the menu⬅️",callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()



def get_setting(ln:str):
    builder = InlineKeyboardBuilder()
    if ln == "Ru":
        builder.button(text="Язык(Language)",callback_data="language")
        builder.button(text="Интерактивные уведомления",callback_data="inter")
        builder.button(text="Вернуться в меню⬅️",callback_data="menu")
    else:
        builder.button(text="Language(Язык)",callback_data="language")
        builder.button(text="Interactive notifications",callback_data="inter")
        builder.button(text="Go back to the menu⬅️",callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()

def get_languages(ln:str):
    builder = InlineKeyboardBuilder()
    if ln == "Ru":
        builder.button(text="Русский(Ru)🇷🇺",callback_data="Ru")
        builder.button(text="Английский(Eu)🇪🇺",callback_data="Eu")
        builder.button(text="Вернуться⬅️",callback_data="setting")
    else:
        builder.button(text="Russian(Ru)🇷🇺",callback_data="Ru")
        builder.button(text="English(Eu)🇪🇺",callback_data="Eu")
        builder.button(text="Back⬅️",callback_data="setting")
    builder.adjust(1)
    return builder.as_markup()

def get_paykeayboard(ln:str):
    builder = InlineKeyboardBuilder()
    builder.button(text="Пожертвовать 20 звезд",pay = True)
    builder.button(text="Отмена🚫",callback_data="delete_pay")
    builder.adjust(1)
    return builder.as_markup()

def get_inline_cancel(ln:str):
    if ln == "Ru":
        inline_kb_list = [
            [InlineKeyboardButton(text="Начать заново🔄",callback_data="repeat")],
            [InlineKeyboardButton(text="Отменить🚫",callback_data="cancel")],
            [InlineKeyboardButton(text="Принять✅",callback_data="commit")]
        ]
    else:
        inline_kb_list = [
            [InlineKeyboardButton(text="Start over🔄🔄",callback_data="repeat")],
            [InlineKeyboardButton(text="Cancel🚫",callback_data="cancel")],
            [InlineKeyboardButton(text="Commit✅",callback_data="commit")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
# Функция для создания клавиатуры с выбором дня
def get_day_keyboard():
    builder = InlineKeyboardBuilder()
    for day in range(1, 32):
        if day < 10:
            builder.button(text=str(day), callback_data="0"+str(day))
        else:
            builder.button(text=str(day), callback_data=str(day))
    builder.adjust(7)  # Разбиваем на строки по 7 кнопок
    return builder.as_markup()

# Функция для создания клавиатуры с выбором месяца
def get_month_keyboard(ln:str):
    if ln == "Ru":
        months = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
    else:
        months = [
            "January", "February","March","April","May","June","Jule",
            "August", "September", "October", "November", "December"
        ]
    builder = InlineKeyboardBuilder()
    for index, month in enumerate(months, start=1):
        if (index < 10):
            builder.button(text=month, callback_data="0"+str(index))
        else:
            builder.button(text=month, callback_data=str(index))
    builder.adjust(3)  # Разбиваем на строки по 3 кнопки
    return builder.as_markup()


def get_all_birthdays(birt_list:list,ln:str):
    builder = InlineKeyboardBuilder()
    for birt in birt_list:
        if ln == "Ru":
            builder.button(text = f"{str(birt[2]).strip()} - {birt[3]} (через {days_until_birthday(birt[3])} день)\n",callback_data=(str(birt[1])))
            builder.adjust(1)
        else:
            builder.button(text = f"{str(birt[2]).strip()} - {birt[3]} (After {days_until_birthday(birt[3])} days)\n",callback_data=(str(birt[1])))
            builder.adjust(1)
    if ln == "Ru":
        builder.button(text="Вернуться в меню⬅️",callback_data="menu")
    else:
        builder.button(text="Go back to the menu⬅️",callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()

def get_return_menu(ln:str):
    builder = InlineKeyboardBuilder()
    if ln == "Ru":
        builder.button(text="Вернуться в меню⬅️",callback_data="menu")
    else:
        builder.button(text="Go back to the menu⬅️",callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()

def get_del_keyboard(ln:str):
    if ln == "Ru":
        inline_kb_list = [
            [InlineKeyboardButton(text="Удалить🗑",callback_data="delete")],
            [InlineKeyboardButton(text="Отменить🚫",callback_data="birthday_list")],
            [InlineKeyboardButton(text="Вернуться в меню⬅️",callback_data="menu")]
        ]
    else:
        inline_kb_list = [
            [InlineKeyboardButton(text="Delete🗑",callback_data="delete")],
            [InlineKeyboardButton(text="Cancel🚫",callback_data="birthday_list")],
            [InlineKeyboardButton(text="Go back to the menu⬅️",callback_data="menu")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def get_inline_repeat(ln:str):
    if ln == "Ru":
        inline_kb_list = [
            [InlineKeyboardButton(text="Начать заново🔄",callback_data="repeat")],
            [InlineKeyboardButton(text="Отменить🚫",callback_data="cancel")],
            [InlineKeyboardButton(text="Повторить добавление🔄",callback_data="commit")]
        ]
    else:
        inline_kb_list = [
            [InlineKeyboardButton(text="Start over🔄",callback_data="repeat")],
            [InlineKeyboardButton(text="Cancel🚫",callback_data="cancel")],
            [InlineKeyboardButton(text="Repeat the addition🔄",callback_data="commit")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)