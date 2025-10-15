import telebot
import yt_dlp
import os

BOT_TOKEN = os.getenv("7128571871:AAGR90GI8BigBA2KLpDFD415VFwiWuZSrao")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎵 Salom! Men Jonibek Music Botman!\n"
                          "Menga YouTube, Instagram yoki TikTok link yuboring 🎧")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    url = message.text
    if "http" in url:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'song.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            for file in os.listdir():
                if file.endswith(".mp3") or file.endswith(".m4a"):
                    bot.send_audio(message.chat.id, open(file, "rb"))
                    os.remove(file)
                    break

        except Exception as e:
            bot.reply_to(message, f"❌ Xatolik yuz berdi: {e}")
    else:
        bot.reply_to(message, "⚠️ Iltimos, to‘g‘ri video link yuboring (YouTube, Instagram, TikTok)!")

print("✅ Bot ishlayapti...")
bot.polling(none_stop=True)
