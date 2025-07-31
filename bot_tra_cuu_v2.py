
import telebot
import pandas as pd

BOT_TOKEN = '8291719250:AAG4eA06fKTJXuuOpQoRWFNOk9kcn7XNtUw'  # ← Thay bằng token bot từ BotFather
bot = telebot.TeleBot(BOT_TOKEN)

# Đọc dữ liệu từ file
df = pd.read_excel("LAL_SUM.xlsx")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Chào bạn! Hãy gửi mã trạm (ví dụ: LAL0423 hoặc lal0423) để tra cứu thông tin.")

@bot.message_handler(func=lambda msg: True)
def tra_cuu_tram(message):

    ma_tram = message.text.strip().upper()
    result = df[df["Name"].str.upper() == ma_tram]

    if result.empty:
        bot.reply_to(message, f"❌ Không tìm thấy mã trạm: {ma_tram}")
    else:
        row = result.iloc[0]
        description = row["Description"]
        team = row["SOS Team"]
        lat = row["Latitude"]
        lon = row["Longitude"]
        gmaps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

        reply = f"""✅ Thông tin trạm:
🔹 Mã trạm: {ma_tram}
🔹 Khu vực: {description}
🔹 Nhóm phụ trách: {team}
📍 [Xem trên Google Maps]({gmaps_link})
"""
        bot.send_message(message.chat.id, reply, parse_mode="Markdown")

bot.polling()
