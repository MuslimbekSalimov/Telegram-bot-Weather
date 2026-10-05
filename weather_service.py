import aiohttp
import asyncio

WEATHER_CODES = {
    0: "Ochiq, musaffo osmon ☀️",
    1: "Asosan ochiq 🌤",
    2: "Qisman bulutli ⛅",
    3: "Bulutli / Qorong'i osmon ☁️",
    45: "Tuman 🌫",
    48: "Muzlagan tuman 🌫❄️",
    51: "Yengil mayda yomg'ir 🌦",
    53: "O'rtacha mayda yomg'ir 🌦",
    55: "Kuchli mayda yomg'ir 🌧",
    61: "Kuchsiz yomg'ir 🌧",
    63: "O'rtacha yomg'ir 🌧",
    65: "Kuchli yomg'ir 🌧🌧",
    71: "Kuchsiz qor 🌨",
    73: "O'rtacha qor ❄️",
    75: "Qalin qor ❄️❄️",
    77: "Qor donalari 🌨",
    80: "Qisqa muddatli yomg'ir 🌦",
    81: "Kuchli jala ⛈",
    82: "O'ta kuchli jala ⛈🌩",
    85: "Kuchsiz qor bo'roni 🌨",
    86: "Kuchli qor bo'roni ❄️🌨",
    95: "Momaqaldiroq 🌩",
    96: "Momaqaldiroq va do'l 🌩🧊",
    99: "Kuchli momaqaldiroq va yirik do'l ⛈🧊"
}

WEATHER_IMAGES = {
    "sunny": "https://images.unsplash.com/photo-1601297183305-6df142704ea2?w=800&q=80",
    "partly_cloudy": "https://images.unsplash.com/photo-1594156596782-656c93e4d504?w=800&q=80",
    "cloudy": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=800&q=80",
    "fog": "https://images.unsplash.com/photo-1487621167305-5d248087c724?w=800&q=80",
    "rain": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=800&q=80",
    "heavy_rain": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800&q=80",
    "snow": "https://images.unsplash.com/photo-1483921020237-2ff51e8e4b22?w=800&q=80",
    "thunderstorm": "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?w=800&q=80",
    "forecast": "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=800&q=80",
    "aqi": "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=800&q=80"
}

def get_weather_image(code: int) -> str:
    """Ob-havo holatiga mos yuqori sifatli rasm URL'i"""
    if code in (0, 1):
        return WEATHER_IMAGES["sunny"]
    elif code == 2:
        return WEATHER_IMAGES["partly_cloudy"]
    elif code == 3:
        return WEATHER_IMAGES["cloudy"]
    elif code in (45, 48):
        return WEATHER_IMAGES["fog"]
    elif code in (51, 53, 55, 61, 80):
        return WEATHER_IMAGES["rain"]
    elif code in (63, 65, 81, 82):
        return WEATHER_IMAGES["heavy_rain"]
    elif code in (71, 73, 75, 77, 85, 86):
        return WEATHER_IMAGES["snow"]
    elif code in (95, 96, 99):
        return WEATHER_IMAGES["thunderstorm"]
    return WEATHER_IMAGES["partly_cloudy"]

PRESET_CITIES = {
    "Toshkent": (41.2995, 69.2401),
    "Samarqand": (39.6542, 66.9597),
    "Buxoro": (39.7747, 64.4286),
    "Andijon": (40.7821, 72.3442),
    "Fargʻona": (40.3842, 71.7843),
    "Namangan": (40.9983, 71.6726),
    "Qarshi": (38.8606, 65.7890),
    "Termiz": (37.2242, 67.2783),
    "Urganch": (41.5500, 60.6333),
    "Nukus": (42.4602, 59.6166),
    "Navoiy": (40.0844, 65.3792),
    "Jizzax": (40.1158, 67.8422),
    "Guliston": (40.4897, 68.7842),
    "Xiva": (41.3783, 60.3639)
}

async def fetch_current_weather(lat: float, lon: float, location_name: str) -> dict:
    """Hozirgi ob-havo ma'lumotlarini olish."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,"
        f"apparent_temperature,weather_code,wind_speed_10m,surface_pressure&timezone=auto"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return {"error": "Ob-havo ma'lumotlarini yuklashda xatolik yuz berdi."}
            data = await resp.json()
            curr = data.get("current", {})
            code = curr.get("weather_code", 0)
            
            return {
                "name": location_name,
                "lat": lat,
                "lon": lon,
                "temp": curr.get("temperature_2m"),
                "feels_like": curr.get("apparent_temperature"),
                "humidity": curr.get("relative_humidity_2m"),
                "wind": curr.get("wind_speed_10m"),
                "pressure": curr.get("surface_pressure"),
                "desc": WEATHER_CODES.get(code, "Ochiq havo"),
                "image_url": get_weather_image(code),
                "time": curr.get("time")
            }

async def fetch_forecast(lat: float, lon: float, location_name: str) -> dict:
    """3 kunlik ob-havo prognozini olish."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,"
        f"temperature_2m_min,sunrise,sunset,uv_index_max&timezone=auto&forecast_days=3"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return {"error": "Prognoz ma'lumotlarini yuklashda xatolik yuz berdi."}
            data = await resp.json()
            daily = data.get("daily", {})
            
            days = []
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            codes = daily.get("weather_code", [])
            sunrises = daily.get("sunrise", [])
            sunsets = daily.get("sunset", [])
            uv_indices = daily.get("uv_index_max", [])

            for i in range(len(dates)):
                day_title = "Bugun" if i == 0 else ("Ertaga" if i == 1 else "Indinga")
                sunrise_time = sunrises[i].split("T")[1] if i < len(sunrises) and "T" in sunrises[i] else "N/A"
                sunset_time = sunsets[i].split("T")[1] if i < len(sunsets) and "T" in sunsets[i] else "N/A"
                code = codes[i] if i < len(codes) else 0

                days.append({
                    "title": day_title,
                    "date": dates[i],
                    "max": max_temps[i] if i < len(max_temps) else "N/A",
                    "min": min_temps[i] if i < len(min_temps) else "N/A",
                    "desc": WEATHER_CODES.get(code, "Ochiq havo"),
                    "sunrise": sunrise_time,
                    "sunset": sunset_time,
                    "uv": uv_indices[i] if i < len(uv_indices) else "N/A"
                })
            
            return {
                "name": location_name,
                "lat": lat,
                "lon": lon,
                "days": days,
                "image_url": WEATHER_IMAGES["forecast"]
            }

async def fetch_air_quality(lat: float, lon: float, location_name: str) -> dict:
    """Havo sifati (AQI, PM2.5, PM10) ma'lumotlarini olish."""
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}&current=pm10,pm2_5,european_aqi&timezone=auto"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return {"error": "Havo sifati ma'lumotlarini yuklashda xatolik yuz berdi."}
            data = await resp.json()
            curr = data.get("current", {})
            aqi = curr.get("european_aqi", 0)
            pm2_5 = curr.get("pm2_5", 0)
            pm10 = curr.get("pm10", 0)

            # AQI baholash
            if aqi <= 20:
                status = "🟢 A'lo darajada toza"
                recommendation = "Ochiq havoda sayr qilish va sport bilan shug'ullanish uchun ideal havo!"
            elif aqi <= 40:
                status = "🟡 Yaxshi / Qoniqarli"
                recommendation = "Havo toza, ko'pchilik uchun hech qanday xavf yo'q."
            elif aqi <= 60:
                status = "🟠 O'rtacha ifloslangan"
                recommendation = "Nafas olish yo'llari sezgir odamlar ochiq havoda uzoq qolmasliklari tavsiya etiladi."
            elif aqi <= 80:
                status = "🔴 Nosog'lom (Yuqori ifloslanish)"
                recommendation = "Hamma uchun noqulay. Niqob taqish va derazalarni yopiq saqlash tavsiya etiladi."
            else:
                status = "🟣 O'ta xavfli daraja!"
                recommendation = "Ko'chaga chiqmaslikka harakat qiling, xona havosini tozalagichdan foydalaning."

            return {
                "name": location_name,
                "lat": lat,
                "lon": lon,
                "aqi": aqi,
                "pm2_5": pm2_5,
                "pm10": pm10,
                "status": status,
                "recommendation": recommendation,
                "image_url": WEATHER_IMAGES["aqi"]
            }

async def search_city_coords(city_name: str):
    """Shahar nomini tekshirish yoki geocoding orqali koordinatasini topish."""
    # Preset viloyatlarni tekshirish
    clean_name = city_name.strip()
    for name, (lat, lon) in PRESET_CITIES.items():
        if name.lower() == clean_name.lower() or name.replace("ʻ", "'").lower() == clean_name.replace("ʻ", "'").lower():
            return lat, lon, name

    # Open-Meteo Geocoding orqali qidirish
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_name}&count=1&language=uz&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(geo_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            results = data.get("results")
            if not results:
                return None
            first = results[0]
            lat = round(first["latitude"], 4)
            lon = round(first["longitude"], 4)
            country = first.get("country", "")
            found_name = f"{first.get('name')}" + (f", {country}" if country else "")
            return lat, lon, found_name

def format_current_weather(data: dict) -> str:
    """Hozirgi ob-havo ma'lumotlarini chiroyli HTML formatda chiqarish."""
    if "error" in data:
        return f"❌ {data['error']}"

    return (
        f"📍 <b>{data['name']}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🌤 <b>Holat:</b> {data['desc']}\n\n"
        f"🌡 <b>Harorat:</b> {data['temp']}°C\n"
        f"🤔 <b>His qilinishi:</b> {data['feels_like']}°C\n"
        f"💧 <b>Namlik:</b> {data['humidity']}%\n"
        f"💨 <b>Shamol tezligi:</b> {data['wind']} km/soat\n"
        f"🧭 <b>Atmosfera bosimi:</b> {data['pressure']} hPa\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"<i>Yangilangan vaqt: {data.get('time', '').replace('T', ' ')}</i>"
    )

def format_forecast(data: dict) -> str:
    """3 kunlik prognozni chiroyli HTML formatda chiqarish."""
    if "error" in data:
        return f"❌ {data['error']}"

    text = f"📅 <b>{data['name']} uchun 3 kunlik ob-havo:</b>\n\n"
    for d in data["days"]:
        text += (
            f"🔸 <b>{d['title']} ({d['date']})</b>\n"
            f"   {d['desc']}\n"
            f"   🌡 Harorat: <b>{d['min']}°C ... {d['max']}°C</b>\n"
            f"   ☀️ Quyosh chiqishi: <code>{d['sunrise']}</code> | Botishi: <code>{d['sunset']}</code>\n"
            f"   🟣 UV indeksi: {d['uv']}\n\n"
        )
    return text.strip()

def format_air_quality(data: dict) -> str:
    """Havo sifati ma'lumotlarini chiqarish."""
    if "error" in data:
        return f"❌ {data['error']}"

    return (
        f"💨 <b>{data['name']} — Havo sifati (AQI)</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Holat: <b>{data['status']}</b>\n"
        f"📊 <b>AQI indeksi:</b> {data['aqi']}\n"
        f"🔹 <b>PM2.5 zarrachalar:</b> {data['pm2_5']} µg/m³\n"
        f"🔹 <b>PM10 zarrachalar:</b> {data['pm10']} µg/m³\n\n"
        f"💡 <b>Tavsiya:</b>\n"
        f"<i>{data['recommendation']}</i>"
    )
