from aiogram import Router,F, Bot
from aiogram.types import Message, CallbackQuery,LabeledPrice
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import asyncio
from database_class import Database
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .idea import create_birt

from inline_kbs import *
from .contexts import Birthday_State,Birthdays_State
from .drlist import return_month,return_week,return_day
from datetime import timedelta, datetime
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
router = Router()
scheduler = AsyncIOScheduler()
db = Database()

@router.message(Command("start"))
async def start_handler(msg:Message,bot:Bot):
    if db.user(msg.from_user.id,msg.chat.id):
        await bot.delete_message(msg.chat.id,msg.message_id)
        if db.get_language(user_id=msg.from_user.id) == "Ru":
            await msg.answer("Привет👋\nЯ буду напоминать тебе про дни рождения🔔\nБуду присылать тебе сообщения за месяц, неделю и день до праздника🎂\nДля начала советую прочитать инструкцию по использованию, она находится в настройках⬇️",reply_markup=get_inline_menu("Ru"))
        else:
            await msg.answer("Hello👋\nI will remind you about birthdays🔔\nI will send you messages a month, a week and a day before the holiday🎂\nFirst, I advise you to read the instructions for use, it is in the settings",reply_markup=get_inline_menu("Eu"))
    else:
        await msg.answer("Невозможно установить соединение(Error 404)")

@router.message(Birthday_State.Name)
async def get_name(msg:Message,state:FSMContext,bot:Bot):
    data = await state.get_data()
    await state.update_data(Name = msg.text)
    await bot.delete_message(msg.chat.id,msg.message_id)
    if db.get_language(user_id=msg.from_user.id) == "Ru":
        await bot.edit_message_text(text = "В какой день?", chat_id = msg.chat.id,message_id = data['mes_id'])
    else:
        await bot.edit_message_text(text = "What day?", chat_id = msg.chat.id,message_id = data['mes_id'])
    await bot.edit_message_reply_markup(chat_id = msg.chat.id, message_id = data['mes_id'],reply_markup=get_day_keyboard())
    await state.set_state(Birthday_State.Day)

@router.callback_query(Birthdays_State.id)
async def del_birthday(call:CallbackQuery,state:FSMContext,bot:Bot):
    if call.data == "menu":
        await check_button(call,state,bot)
        await state.clear()
        return None
    await state.update_data(id = call.data)
    if db.get_language(user_id=call.from_user.id) == "Ru":
        await bot.edit_message_text(text = "Подвердите удаление дня рождения", chat_id = call.message.chat.id,message_id = call.message.message_id)
        await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_del_keyboard("Ru"))
    else:
        await bot.edit_message_text(text = "Confirm deletion of birthday", chat_id = call.message.chat.id,message_id = call.message.message_id)
        await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_del_keyboard("Eu"))
    await state.set_state(Birthdays_State.solution)

@router.callback_query(Birthdays_State.solution)
async def del_birthday(call:CallbackQuery,state:FSMContext,bot:Bot):
    await state.update_data(solution = call.data)
    data = await state.get_data()
    if call.data == "delete":
        if (db.delete_birthday(data['id'])):
            if db.get_language(user_id=call.from_user.id) == "Ru":
                await bot.edit_message_text(text = "День рождения успешно удален", chat_id = call.message.chat.id,message_id = call.message.message_id)
                await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_return_menu("Ru"))
            else:
                await bot.edit_message_text(text = "Birthday successfully deleted", chat_id = call.message.chat.id,message_id = call.message.message_id)
                await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_return_menu("Eu"))
    else:
        await check_button(call,state,bot)
    await state.clear()

@router.callback_query(Birthday_State.Day)
async def get_date(call:CallbackQuery,state:FSMContext,bot:Bot):
    await state.update_data(Day = call.data)
    if db.get_language(user_id=call.from_user.id) == "Ru":
        await bot.edit_message_text(text = "А теперь давайте выберем месяц", chat_id = call.message.chat.id,message_id = call.message.message_id)
        await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_month_keyboard("Ru"))
    else:
        await bot.edit_message_text(text = "Now let's choose a month", chat_id = call.message.chat.id,message_id = call.message.message_id)
        await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_month_keyboard("Eu"))
    await state.set_state(Birthday_State.Month)

@router.callback_query(Birthday_State.Month)
async def get_month(call:CallbackQuery,state:FSMContext,bot:Bot):
    await state.update_data(Month = call.data)
    data = await state.get_data()
    if db.get_language(user_id=call.from_user.id) == "Ru":
        await bot.edit_message_text(text = f"У {data['Name']} день рождения {str(data['Day'])+"."+str(data['Month'])}, всё верно?", chat_id = call.message.chat.id,message_id = call.message.message_id)
        await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_inline_cancel("Ru"))
    else:
        await bot.edit_message_text(text = f"{data['Name']}'s birthday is {str(data['Day'])+"." +str(data['Month'])}, is that correct?", chat_id = call.message.chat.id,message_id = call.message.message_id)
        await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_inline_cancel("Eu"))
    await state.set_state(None)



@router.callback_query()
async def check_button(call:CallbackQuery,state:FSMContext,bot:Bot):
    if call.data == "menu":
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_text(text = "<b>Меню</b>", chat_id = call.message.chat.id,message_id = call.message.message_id)
            await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_inline_menu("Ru"))
        else:
            await bot.edit_message_text(text = "<b>Menu</b>", chat_id = call.message.chat.id,message_id = call.message.message_id)
            await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_inline_menu("Eu"))
        await state.clear()
    if call.data == "setting":
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_text("Настройки (Settings)",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=get_setting("Ru"))
        else:
            await bot.edit_message_text("Settings (Настройки)",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=get_setting("Eu"))
    if call.data == "language":
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_text("Доступные языки (Available languages)",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=get_languages("Ru"))
        else:
            await bot.edit_message_text("Available languages (Доступные языки)",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=get_languages("Eu"))
    if call.data == "Ru":
        db.language(call.from_user.id,"Ru")
        await bot.edit_message_text("Язык успешно изменен на русский",chat_id=call.message.chat.id,message_id=call.message.message_id)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=get_setting("Ru"))
    if call.data == "Eu":
        db.language(call.from_user.id,"Eu")
        await bot.edit_message_text("The language has been successfully changed to English",chat_id=call.message.chat.id,message_id=call.message.message_id)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=get_setting("Eu"))
    if call.data == "birthday_add":
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_text(text = "Кто празднует день рождения?", chat_id = call.message.chat.id,message_id = call.message.message_id)
        else:  
            await bot.edit_message_text(text = "Who is celebrating a birthday?", chat_id = call.message.chat.id,message_id = call.message.message_id)
        await state.set_state(Birthday_State.Name)
        await state.update_data(mes_id = call.message.message_id)
    if call.data == "birthday_list":
        birt_list = db.get_all_birthdays(call.from_user.id)
        if birt_list != False:
            if db.get_language(user_id=call.from_user.id) == "Ru":
                message = "Все дни рождения которые вы добавили:\n(Для удаления нажмите на кнопку)"
                await bot.edit_message_text(message,chat_id=call.message.chat.id,message_id=call.message.message_id)
                await bot.edit_message_reply_markup(chat_id = call.message.chat.id,message_id =  call.message.message_id, reply_markup=get_all_birthdays(birt_list,"Ru"))
            else:
                message = "All the birthdays that you have added:\n(To delete, click on the button)"
                await bot.edit_message_text(message,chat_id=call.message.chat.id,message_id=call.message.message_id)
                await bot.edit_message_reply_markup(chat_id = call.message.chat.id,message_id =  call.message.message_id, reply_markup=get_all_birthdays(birt_list,"Eu"))
            
            await state.set_state(Birthdays_State.id)
    if call.data == "commit":
        data = await state.get_data()
        result = db.insert_birthday(call.from_user.id,data)
        if result:
            if db.get_language(user_id=call.from_user.id) == "Ru":
                message = "День рождения успешно добавлен✅"
            else:
                message = "Birthday added successfully✅"
            await bot.edit_message_text(message,chat_id=call.message.chat.id,message_id=call.message.message_id)
            if db.get_language(user_id=call.from_user.id) == "Ru":
                await bot.edit_message_reply_markup(chat_id = call.message.chat.id,message_id =  call.message.message_id, reply_markup=get_return_menu("Ru"))
            else:
                await bot.edit_message_reply_markup(chat_id = call.message.chat.id,message_id =  call.message.message_id, reply_markup=get_return_menu("Eu"))
            await state.clear()
        else:
            if db.get_language(user_id=call.from_user.id) == "Ru":
                message = "При добавлении появились ошибки😭"
            else:
                message = "Errors appeared when adding😭"
            await bot.edit_message_text(message,chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id = call.message.chat.id,message_id =  call.message.message_id, reply_markup=get_inline_repeat())
    if call.data == "cancel":
        await state.clear()
        if db.get_language(user_id=call.from_user.id) == "Ru":
            message = "Действие отменено, возвращаюсь в меню"
            menu = "<b>Меню</b>"
        else:
            message = "The action is canceled, I return to the menu"
            menu = "<b>Menu</b>"
        await call.answer(message)
        await bot.edit_message_text(text = menu, chat_id = call.message.chat.id,message_id = call.message.message_id)
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_inline_menu("Ru"))
        else: 
            await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id,reply_markup=get_inline_menu("Eu"))
    if call.data == "inter_on":
        db.notifi_on(call.from_user.id)
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_text("Интерактивные уведомления включены🔔",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=notifi_change("Ru"))
        else:
            await bot.edit_message_text("Interactive notifications enabled🔔",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=notifi_change("Eu"))
    if call.data == "inter_off":
        db.notifi_off(call.from_user.id)
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_text("Интерактивные уведомления выключены🔕",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=notifi_change("Ru"))
        else:
            await bot.edit_message_text("Interactive notifications are turned off🔕",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=notifi_change("Eu"))
    if call.data == "repeat":
        await state.clear()
        if db.get_language(user_id=call.from_user.id) == "Ru":
            message = "Кто празднует день рождения?"
        else:
            message = "Who is celebrating a birthday?"
        await bot.edit_message_text(text = message, chat_id = call.message.chat.id,message_id = call.message.message_id)
        await state.set_state(Birthday_State.Name)
        await state.update_data(mes_id = call.message.message_id)
    if call.data == "inter":
        if db.get_language(user_id=call.from_user.id) == "Ru":
            await bot.edit_message_text("Интерактивные уведомления",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=notifi_change("Ru"))
        else:
            await bot.edit_message_text("Interactive notifications",chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=notifi_change("Eu"))
    if call.data == "donate":
        prices = [LabeledPrice(label="XTR", amount=20)]  
        mes = await call.message.answer_invoice(  
            title="Донатик",  
            description="Поддержать разработчиков на 20 звёзд!",  
            prices=prices,  
            provider_token="",  
            payload="bot_support",  
            currency="XTR",  
            reply_markup=get_paykeayboard(),  
        )
    if call.data == "delete_pay":
        await bot.delete_message(call.message.chat.id,call.message.message_id)


async def birthday(bot:Bot):
    user_list = db.get_all_users()
    for user in user_list:
        birt_list = db.get_all_birthdays(user[0])
        for birt in birt_list:
            if (birt[3] == return_month()):
                if db.get_language(user_id=user[0]) == "Ru":
                    await bot.send_message(birt[0],"Через месяц у <b>" + str(birt[2]).strip() +"</b> день рождения - " + birt[3])
                else:
                    await bot.send_message(birt[0],"In a month, <b>" + str(birt[2]).strip() +"</b>  birthday - " + birt[3])
            if (birt[3]== return_week()):
                if db.get_language(user_id=user[0]) == "Ru":
                    await bot.send_message(birt[0],"Через неделю у <b>" + str(birt[2]).strip() +"</b> день рождения - " + birt[3])
                else:
                    await bot.send_message(birt[0],"In a week, <b>" + str(birt[2]).strip() +"</b>  birthday - " + birt[3])
            if (birt[3]== return_day):
                if db.get_language(user_id=user[0]) == "Ru":
                    await bot.send_message(birt[0],"У <b>" + str(birt[2]).strip() +"</b> завтра день рождения!")
                else:
                    await bot.send_message(birt[0],"<b>" + str(birt[2]).strip() +"</b>'s birthday is tomorrow!")
#async def inter_notifi(bot:Bot,user_id:id,name:str,state:FSMContext):

