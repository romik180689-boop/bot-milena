import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    FSInputFile,
)
from aiohttp import web

# ==================== НАСТРОЙКИ ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN не задан!")

HER_NAME = "Милена"
YOUR_NAME = "Рома"

# ==================== ФОТО ====================
PHOTOS = [
    "photo1.jpg",
    "photo2.jpg",
    "photo3.jpg",
    "photo4.jpg",
    "photo5.jpg",
]

# ==================== ПРИЧИНЫ ====================
REASONS = [
    "Твоя улыбка",
    "Искренность",
    "Поддержка",
    "Доброта",
    "Красота и нежность",
    "Забота",
    "Вдохновение",
]

# ==================== ПИСЬМО ====================
LETTER = """Слушай, я тут сидел и считал. 11 месяцев. Это же почти год, представляешь? Казалось бы, только вчера я мялся перед встречей, не зная, как себя вести, а сегодня мы уже самые близкие и знаем друг друга вдоль и поперёк.

Я не мастер красивых речей, ты знаешь. Но сегодня почему-то захотелось написать тебе это не в сообщении, а вот так, чтобы ты перечитала, если вдруг захочешь.

Знаешь, что я понял за эти 11 месяцев? Что с тобой реально легко. Не в том смысле, что мы не ругаемся или всегда всё гладко, нет. Легко в смысле — я могу быть собой. Могу молчать, могу нести какую-то чушь, могу быть уставшим и не смешным, и ты не будешь смотреть на меня как на идиота. Это прекрасно.

Я часто вспоминаю наши первые месяцы. Как мы гуляли и не могли наговориться, как я боялся ляпнуть что-то не то, а потом понял, что с тобой и так всё нормально. Спасибо тебе за то, что ты тогда дала мне это понять.

За эти 11 месяцев было всякое. Были моменты, когда я вёл себя как дурак, и ты терпела. Были моменты, когда мы ссорились из-за ерунды, а потом оба не могли вспомнить, с чего вообще началось. Это нормально, я думаю. Главное, что мы всегда возвращаемся друг к другу. И я это ценю.

Я не знаю, что будет через год или через пять лет. Но я точно знаю, что сейчас, в этот момент, я очень рад, что ты есть. Что именно ты рядом. Что именно с тобой я хочу делиться всякой фигнёй, жаловаться на работу, ржать над тупыми мемами и просто лежать в тишине.

Спасибо тебе за эти 11 месяцев. За твоё терпение, за твой смех, за то, что ты выдерживаешь меня. Я обещаю стараться быть лучше. Ну, по крайней мере, не хуже, чем сейчас.

Люблю тебя."""

# ==================== 20 КОМПЛИМЕНТОВ ====================
COMPLIMENTS = {
    1: "Невероятная",
    2: "Обворожительная",
    3: "Восхитительная",
    4: "Грациозная",
    5: "Притягательная",
    6: "Очаровательная",
    7: "Лучезарная",
    8: "Единственная",
    9: "Неотразимая",
    10: "Божественная",
    11: "Совершенная",
    12: "Элегантная",
    13: "Изумительная",
    14: "Нежная",
    15: "Искренняя",
    16: "Завораживающая",
    17: "Уникальная",
    18: "Превосходная",
    19: "Доброжелательная",
    20: "Неповторимая",
}
# ===================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ==================== ХРАНИЛИЩЕ ПОЛЬЗОВАТЕЛЕЙ ====================
user_state = {}


# ==================== КЛАВИАТУШКИ ====================
def next_kb(callback_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дальше", callback_data=callback_data)],
    ])


def compliment_kb():
    buttons = []
    row = []
    for i in range(1, 21):
        row.append(InlineKeyboardButton(text=str(i), callback_data=f"compl_{i}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def after_compliment_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать ещё", callback_data="show_calendar")],
    ])


# ==================== СТАРТ ====================
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_state[message.from_user.id] = 0

    text = (
        f"Привет, {HER_NAME}.\n\n"
        f"Сегодня у нас с тобой 11 месяцев.\n"
        f"Я подготовил для тебя кое-что.\n\n"
        f"Готова?"
    )
    await message.answer(text, reply_markup=next_kb("start_photos"))


# ==================== ФОТО ====================
@dp.callback_query(F.data == "start_photos")
async def start_photos(call: CallbackQuery):
    user_state[call.from_user.id] = 1
    await send_photo(call.from_user.id, call.message, 0)
    await call.answer()


async def send_photo(user_id, message, index):
    if index >= len(PHOTOS):
        await message.answer(
            "А теперь — причины, почему я тебя люблю.",
            reply_markup=next_kb("start_reasons"),
        )
        return

    photo_file = PHOTOS[index]
    if not os.path.exists(photo_file):
        await message.answer(f"Фото {photo_file} не найдено.")
        await send_photo(user_id, message, index + 1)
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дальше", callback_data=f"next_photo_{index + 1}")],
    ])
    await message.answer_photo(
        FSInputFile(photo_file),
        reply_markup=kb,
    )


@dp.callback_query(F.data.startswith("next_photo_"))
async def next_photo(call: CallbackQuery):
    index = int(call.data.replace("next_photo_", ""))
    await send_photo(call.from_user.id, call.message, index)
    await call.answer()


# ==================== ПРИЧИНЫ ====================
@dp.callback_query(F.data == "start_reasons")
async def start_reasons(call: CallbackQuery):
    await send_reason(call.from_user.id, call.message, 0)
    await call.answer()


async def send_reason(user_id, message, index):
    if index >= len(REASONS):
        await message.answer(
            "А теперь — письмо. Читай не спеша.",
            reply_markup=next_kb("show_letter"),
        )
        return

    reason = REASONS[index]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Дальше", callback_data=f"next_reason_{index + 1}")],
    ])
    await message.answer(
        f"Причина {index + 1} из {len(REASONS)}\n\n{reason}",
        reply_markup=kb,
    )


@dp.callback_query(F.data.startswith("next_reason_"))
async def next_reason(call: CallbackQuery):
    index = int(call.data.replace("next_reason_", ""))
    await send_reason(call.from_user.id, call.message, index)
    await call.answer()


# ==================== ПИСЬМО ====================
@dp.callback_query(F.data == "show_letter")
async def show_letter(call: CallbackQuery):
    await call.message.answer(LETTER, reply_markup=next_kb("start_calendar"))
    await call.answer()


# ==================== КАЛЕНДАРЬ КОМПЛИМЕНТОВ ====================
@dp.callback_query(F.data == "start_calendar")
async def start_calendar(call: CallbackQuery):
    await call.message.answer(
        "А теперь — календарь комплиментов.\n\n"
        "Выбери число от 1 до 20, и я скажу тебе что-то приятное.",
        reply_markup=compliment_kb(),
    )
    await call.answer()


@dp.callback_query(F.data == "show_calendar")
async def show_calendar_again(call: CallbackQuery):
    await call.message.answer(
        "Выбери ещё число.",
        reply_markup=compliment_kb(),
    )
    await call.answer()


@dp.callback_query(F.data.startswith("compl_"))
async def show_compliment(call: CallbackQuery):
    number = int(call.data.replace("compl_", ""))
    text = COMPLIMENTS.get(number, "")

    await call.message.answer(
        f"{number}.\n\n{text}",
        reply_markup=after_compliment_kb(),
    )
    await call.answer()


# ==================== ВЕБ-СЕРВЕР ДЛЯ RENDER ====================
async def handle(request):
    return web.Response(text="Bot is alive!")


async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8080)))
    await site.start()


# ==================== ЗАПУСК ====================
async def main():
    print("Бот для Милены запущен...")
    asyncio.create_task(start_web())
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())