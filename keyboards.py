from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy pastki menyu klaviaturasi."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📍 Hozirgi joylashuvim ob-havosi", request_location=True)
            ],
            [
                KeyboardButton(text="🏙 Viloyatlar bo'yicha"),
                KeyboardButton(text="🇺🇿 Toshkent")
            ],
            [
                KeyboardButton(text="ℹ️ Yordam"),
                KeyboardButton(text="👤 Admin & Reklama")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_admin_inline_keyboard() -> InlineKeyboardMarkup:
    """Admin bilan to'g'ridan-to'g'ri bog'lanish tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Admin bilan bog'lanish", url="https://t.me/salimovv_m")
            ]
        ]
    )

def get_cities_inline_keyboard() -> InlineKeyboardMarkup:
    """O'zbekiston viloyatlari uchun inline tugmalar to'plami."""
    buttons = [
        [
            InlineKeyboardButton(text="Toshkent", callback_data="city:Toshkent"),
            InlineKeyboardButton(text="Samarqand", callback_data="city:Samarqand")
        ],
        [
            InlineKeyboardButton(text="Buxoro", callback_data="city:Buxoro"),
            InlineKeyboardButton(text="Andijon", callback_data="city:Andijon")
        ],
        [
            InlineKeyboardButton(text="Fargʻona", callback_data="city:Fargʻona"),
            InlineKeyboardButton(text="Namangan", callback_data="city:Namangan")
        ],
        [
            InlineKeyboardButton(text="Qarshi", callback_data="city:Qarshi"),
            InlineKeyboardButton(text="Termiz", callback_data="city:Termiz")
        ],
        [
            InlineKeyboardButton(text="Urganch", callback_data="city:Urganch"),
            InlineKeyboardButton(text="Nukus", callback_data="city:Nukus")
        ],
        [
            InlineKeyboardButton(text="Navoiy", callback_data="city:Navoiy"),
            InlineKeyboardButton(text="Jizzax", callback_data="city:Jizzax")
        ],
        [
            InlineKeyboardButton(text="Guliston", callback_data="city:Guliston"),
            InlineKeyboardButton(text="Xiva", callback_data="city:Xiva")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_weather_details_keyboard(lat: float, lon: float, name: str, current_view: str = "current") -> InlineKeyboardMarkup:
    """
    Ob-havo xabari ostidagi interaktiv tugmalar.
    Telegram callback_data 64 bayt chegarasiga e'tibor qaratilgan.
    """
    clean_lat = round(lat, 3)
    clean_lon = round(lon, 3)
    safe_name = name.replace(":", "-")[:20]

    first_row = []
    if current_view == "current":
        first_row.append(InlineKeyboardButton(text="🔄 Yangilash", callback_data=f"curr:{clean_lat}:{clean_lon}:{safe_name}"))
        first_row.append(InlineKeyboardButton(text="📅 3 kunlik prognoz", callback_data=f"fc:{clean_lat}:{clean_lon}:{safe_name}"))
    elif current_view == "forecast":
        first_row.append(InlineKeyboardButton(text="🌤 Hozirgi holat", callback_data=f"curr:{clean_lat}:{clean_lon}:{safe_name}"))
        first_row.append(InlineKeyboardButton(text="💨 Havo sifati", callback_data=f"aqi:{clean_lat}:{clean_lon}:{safe_name}"))
    elif current_view == "aqi":
        first_row.append(InlineKeyboardButton(text="🌤 Hozirgi holat", callback_data=f"curr:{clean_lat}:{clean_lon}:{safe_name}"))
        first_row.append(InlineKeyboardButton(text="📅 3 kunlik prognoz", callback_data=f"fc:{clean_lat}:{clean_lon}:{safe_name}"))

    second_row = []
    if current_view == "current":
        second_row.append(InlineKeyboardButton(text="💨 Havo sifati (AQI)", callback_data=f"aqi:{clean_lat}:{clean_lon}:{safe_name}"))
    second_row.append(InlineKeyboardButton(text="🏙 Boshqa viloyatlar", callback_data="list_cities"))

    rows = [first_row, second_row]
    return InlineKeyboardMarkup(inline_keyboard=rows)
