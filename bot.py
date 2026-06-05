import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات البوت
TOKEN = "8787661226:AAHm-lgdRthuzeXxusc8ffwZiB0OUZhHzmc"
AMAZON_TAG = "alhamzistore-21"

# المنتجات التجريبية
PRODUCTS = {
    "ايفون": [
        {"site": "أمازون 🟠", "price": "4,299 ر.س", "url": f"https://amazon.sa/s?k=iphone&tag={AMAZON_TAG}"},
        {"site": "نون 🟡", "price": "4,199 ر.س", "url": "https://noon.com/saudi-ar/search?q=iphone"},
    ],
    "سامسونج": [
        {"site": "أمازون 🟠", "price": "3,299 ر.س", "url": f"https://amazon.sa/s?k=samsung&tag={AMAZON_TAG}"},
        {"site": "نون 🟡", "price": "3,199 ر.س", "url": "https://noon.com/saudi-ar/search?q=samsung"},
    ],
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 أهلاً! أنا صياد الأسعار 🇸🇦\n\n"
        "اكتب اسم أي منتج وأعطيك أفضل الأسعار!\n\n"
        "جرب: ايفون | سامسونج"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    results = None
    
    for key in PRODUCTS:
        if key in query:
            results = PRODUCTS[key]
            break
    
    if results:
        msg = f"🔍 نتائج البحث عن: {query}\n\n"
        for r in results:
            msg += f"{r['site']}\n💰 {r['price']}\n🔗 {r['url']}\n\n"
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("😔 ما لقيت نتائج. جرب: ايفون | سامسونج")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    print("✅ البوت شغال!")
    app.run_polling()

if __name__ == "__main__":
    main()