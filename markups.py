from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ----------Main_Button--------
mainMenu = InlineKeyboardMarkup(row_width=2)
btnBuySMS = InlineKeyboardButton(text="Купить номер", callback_data="BuySMS")
btnBalance = InlineKeyboardButton(text="Балланс", callback_data="btnBalance")
mainMenu.insert(btnBuySMS)
mainMenu.insert(btnBalance)

# -----------Buy_Service----------
Buy_Service = InlineKeyboardMarkup(row_width=2)
btnBuyDelivery = InlineKeyboardMarkup(text="Delivery Club", callback_data="buyDelivery")
btnReturnMain = InlineKeyboardMarkup(text="Главное меню", callback_data="mainMenu")
Buy_Service.insert(btnBuyDelivery)
Buy_Service.insert(btnReturnMain)
btnReturnMain = InlineKeyboardMarkup

# ---------- Select_service -------
menuService = InlineKeyboardMarkup(row_width=2)
btnBuySMSDelivery = InlineKeyboardButton(text="Купить номер", callback_data="BuyNum_MR")
btnCheckSMS = InlineKeyboardButton(text="Получить SMS", callback_data="btnCheckSMS")
btnNoSMS = InlineKeyboardButton(text="SMS Не пришла", callback_data="btnNoSMS")
btnCancelNum = InlineKeyboardButton(text="Отменить номер", callback_data="btnCancelNum")
btnExtend = InlineKeyboardButton(text="Получить еще SMS", callback_data="btnExtend")
btnReturnMain = InlineKeyboardMarkup(text="Главное меню", callback_data="mainMenu")
btnTEST = InlineKeyboardMarkup(text="TEST", callback_data="TEST")


menuService.insert(btnBuySMSDelivery)
menuService.insert(btnCheckSMS)
menuService.insert(btnNoSMS)
menuService.insert(btnCancelNum)
menuService.insert(btnExtend)
menuService.insert(btnReturnMain)
btnReturnMain = InlineKeyboardMarkup
menuService.insert(btnTEST)
# ----------- Main -----------
