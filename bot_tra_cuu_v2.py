import telebot
import pandas as pd

BOT_TOKEN = "8291719250:AAG4eA06fKTJXuuOpQoRWFNOk9kcn7XNtUw"  # 🔒 Thay bằng token thật từ BotFather
bot = telebot.TeleBot(BOT_TOKEN)

df = pd.read_excel("LAL_SUM.xlsx")
df.columns = [col.strip().lower() for col in df.columns]

def tra_cuu(keyword):
    keyword = str(keyword).lower().strip()
    matched = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(keyword).any(), axis=1)]
    if matched.empty:
        return "❌ Không tìm thấy thông tin phù hợp."
    results = []
    for _, row in matched.iterrows():
        text = "\n".join([f"{col.title()}: {row[col]}" for col in df.columns])
        if "lat" in row and "lon" in row:
            try:
                lat, lon = float(row["lat"]), float(row["lon"])
                text += f"\n📍 Vị trí: https://maps.google.com/?q={lat},{lon}"
            except:
                pass
        results.append(text)
    return "\n\n---\n\n".join(results[:5])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn 👋! Gửi tôi từ khoá hoặc mã trạm để tra cứu thông tin.")

@bot.message_handler(func=lambda message: True)
def handle_query(message):
    keyword = message.text
    result = tra_cuu(keyword)
    bot.reply_to(message, result)

print("🤖 Bot đang chạy...")
bot.polling()
