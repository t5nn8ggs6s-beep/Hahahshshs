import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

TOKEN = os.getenv("8736878861:AAF0tgDvKokvf-YOjPx585EpaljrEWQG9lM")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Первая картинка при старте
    photo = types.FSInputFile("image.png")
    kb = [
        [types.InlineKeyboardButton(text="Купить", callback_data="show_buy_info")],
        [types.InlineKeyboardButton(text="Начать сначала", callback_data="restart")]
    ]
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer_photo(
        photo,
        caption="Привет, житель! Ты пришел за покупкой? Обучиться телекинезу ты можешь тут.",
        reply_markup=reply_markup
    )

@dp.callback_query(F.data == "restart")
async def restart(callback: types.CallbackQuery):
    await start_handler(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "show_buy_info")
async def show_buy_info(callback: types.CallbackQuery):
    # Вторая картинка перед оплатой
    photo2 = types.FSInputFile("image2.png")
    
    # Отправляем фото с описанием
    await callback.message.answer_photo(
        photo2,
        caption="Хорошо, что решил купить наш товар! В наличии есть только тариф навсегда."
    )
    
    # Сразу выставляем счет на 130 звезд
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Тариф Навсегда",
        description="Полный доступ к курсу телекинеза",
        payload="telekinesis_forever",
        currency="XTR",
        prices=[LabeledPrice(label="Оплата звездами", amount=130)]
    )
    await callback.answer()

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    # Подтверждаем готовность принять платеж
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def success_payment(message: types.Message):
    # После покупки ничего не пишем (или просто подтверждаем в логах)
    pass

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
