import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8787661226:AAHm-lgdRthuzeXxusc8ffwZiB0OUZhHzmc"
GEMINI_KEY = "AQ.Ab8RN6ImMepNwUJd1dE4-b_JIZdY7vvR2b_51VyMrM8Qg2PtxA"
AMAZON_TAG = "alhamzistore-21"

logging.basicConfig(level=logging.INFO)

async def ask_gemini(query: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    prompt = f"""أنت مساعد تسوق ذكي. المستخدم يبحث عن: {query}
تعرف على لغة المستخدم وارد عليه بنفس لغته.
قدم:
1. اقتراح أفضل منتج مناسب
2. وصف بسيط للمنتج
3. رابط البحث: https://amazon.sa/s?k={query.replace(' ', '+')}&tag={AMAZON_TAG}
كن مختصراً وودودا."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        }, timeout=30)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 أهلاً! أنا صياد الأسعار الذكي 🇸🇦\n\nأخبرني وش تبي تشتري؟ 🛒"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text("🔍 جاري البحث...")
    result = await ask_gemini(query)
    await update.message.reply_text(result)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
print("✅ البوت الذكي شغال!")
app.run_polling()
