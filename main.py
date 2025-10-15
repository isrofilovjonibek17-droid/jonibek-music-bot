import teleboimport telebot
import yt_dlp
import os

# 🔑 Bot tokeningni shu joyga yoz
BOT_TOKEN = "7128571871:AAGR90GI8BigBA2KLpDFD415VFwiWuZSrao"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎧 Salom, men Jonibek Musiqa botman!\n"
        "Menga YouTube, TikTok yoki Instagram link yubor — men uni yuklab beraman va nomi bilan saqlayman 🎵"
    )

@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "❌ Iltimos, to‘liq video yoki qo‘shiq linkini yubor.")
        return

    bot.reply_to(message, "⏳ Yuklab olayapman, biroz kuting...")

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",  # Fayl nomi avtomatik qo‘shiq nomi bo‘ladi
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            base, _ = os.path.splitext(file_name)
            mp3_file = base + ".mp3"

        with open(mp3_file, "rb") as audio:
            bot.send_audio(message.chat.id, audio, title=info.get("title", "Qo‘shiq"))

        os.remove(mp3_file)
        bot.send_message(message.chat.id, f"✅ Yuklab bo‘ldi: {info.get('title', 'Noma’lum')}")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Xato yuz berdi:\n{e}")

bot.polling()

