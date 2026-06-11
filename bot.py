import logging
import httpx
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
AMAZON_TAG = os.environ.get("AMAZON_TAG")

logging.basicConfig(level=logging.INFO)

async def ask_ai(query: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"""أنت مساعد تسوق ذكي. المستخدم يبحث عن: {query}
تعرف على لغة المستخدم وارد عليه بنفس لغته.
قدم:
1. اقتراح أفضل منتج مناسب
2. وصف بسيط للمنتج
3. رابط البحث: https://amazon.sa/s?k={query.replace(' ', '+')}&tag={AMAZON_TAG}
كن مختصراً وودوداً."""
                        }
                    ]
                },
                timeout=30
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"AI error: {e}")
        return "❌ حدث خطأ، حاول مرة ثانية."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 أهلاً! أنا صياد الأسعار الذكي 🇸🇦\n\nأخبرني وش تبي تشتري؟ 🛒"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text("🔍 جاري البحث...")
    result = await ask_ai(query)
    await update.message.reply_text(result)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
print("✅ البوت الذكي شغال!")
app.run_polling(drop_pending_updates=True)
