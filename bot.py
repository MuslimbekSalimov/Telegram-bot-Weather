import asyncio
import logging
import socket
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart, Command
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError

from config import BOT_TOKEN, check_token

class IPv4AiohttpSession(AiohttpSession):
    """Windows va ayrim provayderlarda IPv6 semaphore timeout xatoligini oldini olish uchun IPv4 sessiyasi."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connector_init["family"] = socket.AF_INET
from weather_service import (
    search_city_coords,
    fetch_current_weather,
    fetch_forecast,
    fetch_air_quality,
    format_current_weather,
    format_forecast,
    format_air_quality,
    PRESET_CITIES
)
from keyboards import (
    get_main_reply_keyboard,
    get_cities_inline_keyboard,
    get_weather_details_keyboard
)

# Windows konsolida emojilar va xabarlar to'g'ri chiqishi uchun
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """Foydalanuvchi /start bosganida ishga tushadi."""
    user_name = message.from_user.first_name or "Do'stim"
    
    # Toshkent bo'yicha dastlabki ob-havo
    lat, lon = PRESET_CITIES["Toshkent"]
    curr_data = await fetch_current_weather(lat, lon, "Toshkent")
    weather_text = format_current_weather(curr_data)

    welcome_text = (
        f"👋 Assalomu alaykum, <b>{user_name}</b>!\n"
        f"Ob-havo ma'lumotlari botiga xush kelibsiz! 🌤\n\n"
        f"👇 <b>Bugungi Toshkent shahri ob-havosi:</b>\n\n"
        f"{weather_text}\n\n"
        f"💡 <i>Quyidagi tugmalar orqali viloyatlarni tanlashingiz, o'z joylashuvingizni yuborishingiz yoki istalgan shahar nomini (masalan: Samarqand, Parij, London) yozib yuborishingiz mumkin!</i>"
    )

    await message.answer(
        text=welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_reply_keyboard()
    )

@dp.message(Command("help"))
@dp.message(F.text == "ℹ️ Yordam")
async def handle_help(message: types.Message):
    """Yordam bo'limi."""
    help_text = (
        "📖 <b>Botdan foydalanish bo'yicha qo'llanma:</b>\n\n"
        "1️⃣ <b>📍 Hozirgi joylashuvim:</b> Pastdagi tugmani bosing va botga o'z koordinatangizni yuboring. Bot siz turgan nuqtadagi ob-havoni aniqlab beradi.\n"
        "2️⃣ <b>🏙 Viloyatlar:</b> 'Viloyatlar bo'yicha' tugmasini bosib O'zbekistonning istalgan viloyatini tanlang.\n"
        "3️⃣ <b>✍️ Matn orqali qidiruv:</b> Dunyoning istalgan shahar yoki tuman nomini shunchaki xabar sifatida yozib yuboring (masalan: <i>Urganch</i>, <i>Zarafshon</i>, <i>Istanbul</i>, <i>Dubay</i>).\n"
        "4️⃣ <b>📅 3 kunlik prognoz va 💨 Havo sifati (AQI):</b> Har bir ob-havo ma'lumoti ostidagi tugmalar orqali ko'p kunlik prognoz va havodagi chang miqdorini ko'rishingiz mumkin."
    )
    await message.answer(help_text, parse_mode=ParseMode.HTML)

@dp.message(F.text == "🏙 Viloyatlar bo'yicha")
async def show_cities(message: types.Message):
    """Viloyatlar ro'yxatini chiqarish."""
    await message.answer(
        text="Kerakli viloyatni tanlang: 👇",
        reply_markup=get_cities_inline_keyboard()
    )

@dp.message(F.text == "🇺🇿 Toshkent")
async def show_tashkent(message: types.Message):
    """Toshkent ob-havosi."""
    lat, lon = PRESET_CITIES["Toshkent"]
    curr = await fetch_current_weather(lat, lon, "Toshkent")
    text = format_current_weather(curr)
    kb = get_weather_details_keyboard(lat, lon, "Toshkent", "current")
    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb)

@dp.callback_query(F.data.startswith("city:"))
async def handle_city_callback(callback: types.CallbackQuery):
    """Inline tugmalardan viloyat bosilganda."""
    city_name = callback.data.split(":")[1]
    await callback.answer(f"{city_name} ob-havosi yuklanmoqda...")
    
    coords = await search_city_coords(city_name)
    if not coords:
        await callback.message.answer(f"❌ '{city_name}' bo'yicha ma'lumot topilmadi.")
        return
        
    lat, lon, name = coords
    curr = await fetch_current_weather(lat, lon, name)
    text = format_current_weather(curr)
    kb = get_weather_details_keyboard(lat, lon, name, "current")

    await callback.message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb)

@dp.callback_query(F.data == "list_cities")
async def handle_list_cities_callback(callback: types.CallbackQuery):
    """Boshqa viloyatlar inline tugmasi bosilganda."""
    await callback.answer()
    await callback.message.answer(
        text="Kerakli viloyatni tanlang: 👇",
        reply_markup=get_cities_inline_keyboard()
    )

@dp.callback_query(F.data.startswith("curr:"))
async def handle_curr_callback(callback: types.CallbackQuery):
    """Hozirgi ob-havoni yangilash yoki ko'rish."""
    await callback.answer("Ob-havo yangilanmoqda...")
    parts = callback.data.split(":")
    lat = float(parts[1])
    lon = float(parts[2])
    name = parts[3]

    curr = await fetch_current_weather(lat, lon, name)
    text = format_current_weather(curr)
    kb = get_weather_details_keyboard(lat, lon, name, "current")

    try:
        await callback.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=kb)
    except TelegramBadRequest:
        pass  # Xabar mazmuni o'zgarmagan bo'lsa xatolik bermaydi

@dp.callback_query(F.data.startswith("fc:"))
async def handle_forecast_callback(callback: types.CallbackQuery):
    """3 kunlik prognozni ko'rish."""
    await callback.answer("Prognoz yuklanmoqda...")
    parts = callback.data.split(":")
    lat = float(parts[1])
    lon = float(parts[2])
    name = parts[3]

    fc = await fetch_forecast(lat, lon, name)
    text = format_forecast(fc)
    kb = get_weather_details_keyboard(lat, lon, name, "forecast")

    try:
        await callback.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=kb)
    except TelegramBadRequest:
        pass

@dp.callback_query(F.data.startswith("aqi:"))
async def handle_aqi_callback(callback: types.CallbackQuery):
    """Havo sifati (AQI) ma'lumotlarini ko'rish."""
    await callback.answer("Havo sifati ma'lumotlari yuklanmoqda...")
    parts = callback.data.split(":")
    lat = float(parts[1])
    lon = float(parts[2])
    name = parts[3]

    aq = await fetch_air_quality(lat, lon, name)
    text = format_air_quality(aq)
    kb = get_weather_details_keyboard(lat, lon, name, "aqi")

    try:
        await callback.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=kb)
    except TelegramBadRequest:
        pass

@dp.message(F.location)
async def handle_location(message: types.Message):
    """Foydalanuvchi GPS joylashuv yuborganida."""
    lat = message.location.latitude
    lon = message.location.longitude
    name = "📍 Joylashuvingiz"

    curr = await fetch_current_weather(lat, lon, name)
    text = format_current_weather(curr)
    kb = get_weather_details_keyboard(lat, lon, name, "current")
    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb)

@dp.message(F.text)
async def handle_city_search(message: types.Message):
    """Foydalanuvchi istalgan shahar nomini yozib yuborganida."""
    city_query = message.text.strip()
    status_msg = await message.answer(f"🔍 <i>'{city_query}'</i> bo'yicha ob-havo qidirilmoqda...", parse_mode=ParseMode.HTML)
    
    coords = await search_city_coords(city_query)
    if not coords:
        await status_msg.edit_text(
            f"❌ <b>'{city_query}'</b> shahri yoki joylashuvi topilmadi.\n\n"
            f"Iltimos, shahar nomini to'g'ri yozganingizni tekshiring (masalan: <i>Samarqand</i>, <i>Buxoro</i>, <i>Parij</i>).",
            parse_mode=ParseMode.HTML
        )
        return

    lat, lon, name = coords
    curr = await fetch_current_weather(lat, lon, name)
    text = format_current_weather(curr)
    kb = get_weather_details_keyboard(lat, lon, name, "current")

    await status_msg.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=kb)

async def main():
    check_token()
    session = IPv4AiohttpSession(timeout=60.0)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session
    )
    print("=" * 50)
    print("🤖 Ob-havo Telegram boti muvaffaqiyatli ishga tushdi!")
    print("Xabarlarni qabul qilish boshlandi...")
    print("=" * 50)

    while True:
        try:
            await dp.start_polling(bot)
            break
        except (TelegramNetworkError, asyncio.TimeoutError) as exc:
            logging.warning(f"Tarmoq uzilishi yuz berdi ({exc}). 5 soniyadan keyin qayta ulanadi...")
            await asyncio.sleep(5)
        except Exception as exc:
            logging.error(f"Kutilmagan xatolik: {exc}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Bot to'xtatildi.")
