# 🌤 Telegram Ob-havo Boti (Weather Bot)

Ushbu bot Telegram orqali real vaqtdagi ob-havo ma'lumotlari, 3 kunlik batafsil ob-havo prognozi hamda havo sifati (AQI) ko'rsatkichlarini taqdim etuvchi zamonaviy Python boti hisoblanadi.

---

## ✨ Imkoniyatlari:
- 🚀 **Tezkor start:** `/start` buyrug'i berilganda darhol Toshkent shahri ob-havosi ko'rsatiladi.
- 📍 **GPS Joylashuv:** *"📍 Hozirgi joylashuvim ob-havosi"* tugmasi bosilganda o'zingiz turgan nuqtaning aniq koordinatalari bo'yicha ob-havo olinadi.
- 🏙 **Viloyatlar ro'yxati:** O'zbekistonning barcha 14 ta hududi (Toshkent, Samarqand, Buxoro, Andijon, Fargʻona, Namangan, Qarshi, Termiz, Urganch, Nukus, Navoiy, Jizzax, Guliston, Xiva) uchun qulay inline tugmalar.
- 🔍 **Istalgan shahar qidiruvi:** Shahar yoki tuman nomini (masalan: *Chirchiq*, *Shahrisabz*, *Parij*, *London*, *Dubay*) shunchaki matn sifatida yozib yuborish kifoya.
- 📅 **3 kunlik prognoz:** Harorat diapazoni, quyosh chiqishi va botishi vaqtlari, ultrabinafsha (UV) nurlanish indeksi.
- 💨 **Havo sifati (AQI):** PM2.5 va PM10 chang zarrachalari miqdori hamda salomatlik uchun tavsiyalar.
- ⚡️ **Mutlaqo bepul:** Open-Meteo ochiq API xizmatidan foydalanadi (hech qanday to'lov yoki ob-havo API kaliti talab qilinmaydi).

---

## 🚀 Ishga tushirish bo'yicha qo'llanma:

### 1-qadam: Telegram Bot Token olish
1. Telegramda [@BotFather](https://t.me/BotFather) botini oching.
2. `/newbot` buyrug'ini yuboring.
3. Botingizga istalgan nom (masalan: `Mening Ob Havo Botim`) va username (masalan: `obhavo_test_123_bot`) bering.
4. BotFather taqdim etgan **API Token**ni nusxalab oling (masalan: `7123456789:AAEjf8X...`).

### 2-qadam: Tokenni `.env` fayliga kiritish
Loyiha papkasidagi `.env` faylini oching va tokenni yozing:
```env
BOT_TOKEN=Sizning_Bot_Tokeningiz_Shu_Yerga
```

### 3-qadam: Botni ishga tushirish
Ushbu papkada terminal ochib quyidagi buyruqni bering:
```powershell
.\.venv\Scripts\python.exe bot.py
```
Yoki shunchaki papkadagi **`run.bat`** fayliga sichqoncha bilan 2 marta bosing!
