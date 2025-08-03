
import telebot
import pandas as pd
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN không được thiết lập trong biến môi trường.")
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
        tl = row["Nombre TL"]
        cellular = row["Cellular"]
        lat = row["Latitude"]
        lon = row["Longitude"]
        gmaps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

        reply = f"""✅ Thông tin trạm:
🔹 Mã trạm: {ma_tram}
🔹 Khu vực: {description}
🔹 Nhóm phụ trách: {team}
🔹 Nhóm trưởng: {tl}
🔹 SĐT Nhóm trưởng: {cellular}
📍 [Xem trên Google Maps]({gmaps_link})
"""
        bot.send_message(message.chat.id, reply, parse_mode="Markdown")

print("🤖 Bot đang chạy...")
bot.polling()
