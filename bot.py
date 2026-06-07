import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8787661226:AAHm-lgdRthuzeXxusc8ffwZiB0OUZhHzmc"
GEMINI_KEY = "AIzaSyAQ.Ab8RN6LvoLGEXBekBz-rYw-tG5qietyS0Eg99WbvjPZs9VwwmQ"
AMAZON_TAG = "alhamzistore-21"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 أهلاً! أنا صياد الأسعار الذكي 🇸🇦\n\nأخبرني وش تبي تشتري؟ وأنا أساعدك تلاقي أفضل منتج بأفضل سعر على أمازون! 🛒"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text("🔍 جاري البحث...")
    
    prompt = f"""أنت مساعد تسوق ذكي. المستخدم يبحث عن: {query}

تعرف على لغة المستخدم وارد عليه بنفس لغته تلقائياً.

قدم:
1. اقتراح أفضل منتج مناسب
2. وصف بسيط للمنتج
3. رابط البحث: https://amazon.sa/s?k={query.replace(' ', '+')}&tag={AMAZON_TAG}

كن مختصراً وودوداً."""

    response = model.generate_content(prompt)
    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
print("✅ البوت الذكي شغال!")
app.run_polling()
