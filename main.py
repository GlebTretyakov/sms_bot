import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
from db import Database



TOKEN = "5901712995:AAFomV6_etWlP6sMMQ613BNDlaXKafnqAmY"
LAVA_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI1NjgyZDUzMC0xMDBjLWI5YmUtYTdhNS04YWM3NmVmMTAwNGEiLCJ0aWQiOiJhZjgxYTY0My00MWFjLTE4YTgtYTNmYS1hMjcyMDcxOGZhMjYifQ.0BhWzritVoYLfs4R2ebwt27rIAIrZBTY_0Eiw5IZaQA"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


def get_number():  # Получение номера
    method = "getNumber"
    VAK_token = "15d76a4fd78c41c5bf5b138ebe4389c0"
    url = f"https://vak-sms.com/api/{method}/?apiKey={VAK_token}&service=mr&country=ru&operator=mtt"
    response = requests.get(url)
    return response.json()


def get_sms(idNum):  # Получение SMS
    method = "getSmsCode"
    VAK_token = "15d76a4fd78c41c5bf5b138ebe4389c0"
    url = f"https://vak-sms.com/api/{method}/?apiKey={VAK_token}&idNum={idNum}"
    response = requests.get(url)
    return response.json()

def extend_num(idNum): # Продление номера
    method = "setStatus"
    send = "send"
    VAK_token = "15d76a4fd78c41c5bf5b138ebe4389c0"
    url = f"https://vak-sms.com/api/{method}/?apiKey={VAK_token}&status={send}&idNum={idNum}"
    response = requests.get(url)
    return response.json()

def cancel_num(idNum): # Отмена номера (изменение статуса номера)
    method = "setStatus"
    VAK_token = "15d76a4fd78c41c5bf5b138ebe4389c0"
    url = f"https://vak-sms.com/api/{method}/?apiKey={VAK_token}&status=end&idNum={idNum}"
    response = requests.get(url)
    return response.json()


@dp.message_handler(commands=['start']) # запуск бота
async def start(message: types.Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Бот по получении SMS", reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, "Бот по получении SMS", reply_markup=nav.mainMenu)


@dp.callback_query_handler()
async def vote_callback(call: types.CallbackQuery):
# -----------------------покупка SMS----------------------
    if call.data == 'BuySMS':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.message.answer("Выберите сервис:", reply_markup=nav.Buy_Service)
    elif call.data == 'buyDelivery': # выбор в меню деливери
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.message.answer("Delivery Club", reply_markup=nav.menuService)
    elif call.data == 'BuyNum_MR': # покупка номера делевери
        if db.get_active_num(call.from_user.id) == str(0):
            db.set_active_num(call.from_user.id, 1)
            db.set_one_sms(call.from_user.id, str(0))
            await call.answer("Вы купили номер для Delivery Club, ожидайте получение номера", show_alert=True)
            await call.message.answer("Вы купили номер для Delivery Club, ожидайте получение номера...")
            await bot.delete_message(call.from_user.id, call.message.message_id)
            response_get_number = get_number()
            phone = response_get_number["tel"]
            idNum = response_get_number["idNum"]
            print(phone, "\n" + idNum)
            db.set_phone(call.from_user.id, response_get_number["tel"])
            db.set_idNum(call.from_user.id, response_get_number["idNum"])
            await call.message.answer("Ваш номер: " + str(phone)[1:], reply_markup=nav.menuService)
        else:
            await call.answer("Вы не можете купить новый номер.\nОтмените ваш прошлый номер и тогда сможете купить новый номер", show_alert=True)

#-------------------------Получение SMS ---------

    elif call.data == 'btnCheckSMS':
        try:
            if get_sms(db.get_idNum(call.from_user.id))["smsCode"] is None:
                await bot.send_message(call.from_user.id, "SMS НЕТ!")
            else:
                sms = get_sms(db.get_idNum(call.from_user.id))["smsCode"]
                db.set_sms(call.from_user.id, sms)
                if db.get_one_sms(call.from_user.id) == str(0):
                    db.set_one_sms(call.from_user.id, str(1))
                    await call.message.answer("Ваш код: " + db.get_sms(call.from_user.id))
                    await call.message.answer("Вы можете получить ещё смс на этот номер в течение 20 минут")
                else:
                    await call.message.answer("Ваш код: " + db.get_sms(call.from_user.id))


        except:
            await call.message.answer("У вас нет сообщений")

#----------------------- Отмена номера --------------
    elif call.data == 'btnCancelNum':
        if db.get_active_num(call.from_user.id) == str(1):
            try:
                if get_sms(db.get_idNum(call.from_user.id))["smsCode"] is None:
                    cancel_num(db.get_idNum(call.from_user.id))
                    db.set_active_num(call.from_user.id, str(0))
                    db.set_active_sms(call.from_user.id, str(0))
                    await call.answer("Вы отменили свой номер, деньги вернуться на баланс", show_alert=True)
                    await call.answer("Вы отменили свой номер, деньги вернуться на баланс",
                                      reply_markup=nav.menuService)
                else:
                    await call.answer("Вам поступила SMS, деньги \nза отмену не вернуться!", show_alert=True)
                    db.set_active_num(call.from_user.id, str(0))
            except:
                await call.answer("уххххх...")


        elif db.get_active_num(call.from_user.id) == str(0):
            await call.answer("У вас нет активного номера", show_alert=True)

    elif call.data == 'btnExtend':
        extend_num(db.get_idNum(call.from_user.id))
        db.set_active_num(call.from_user.id, 1)
        await call.answer("Вы можете получить следующую SMS\n", show_alert=True)

#--------------Смс не пришла?----------

    elif call.data == 'btnNoSMS':
        await call.answer("Если в течении 3ех минут смс не пришла, то \nотмените номер и купите новый!", show_alert=True)

# ---------------------- Выход в главное меню -----------------
    elif call.data == 'mainMenu':
        await call.message.answer("Главное меню", reply_markup=nav.mainMenu)
        # await bot.delete_message(call.from_user.id, call.message.message_id)
    else:
        await call.message.answer("HUY")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
