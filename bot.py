import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import keep_alive

TELEGRAM_TOKEN = "8193262941:AAF1P-o_LISQfl-PYiU26tBTk8jaIaqQVFs"
AFFILIATE_API_ID = "514130"
AFFILIATE_API_KEY = "nV8vFBa61NIsLcx2KOgJjoRByzmIfnO0"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل كلمة للبحث عن المنتجات في AliExpress:")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("من فضلك أدخل كلمة للبحث.")
        return
    url = f"https://api.aliexpressaffiliate.com/v2/search?app_key={AFFILIATE_API_KEY}&tracking_id={AFFILIATE_API_ID}&keywords={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("result", {}).get("products", [])
        if results:
            reply = "

".join([f"{p['product_title']}
{p['product_url']}" for p in results[:5]])
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("لا توجد نتائج.")
    else:
        await update.message.reply_text("حدث خطأ في جلب النتائج.")

def main():
    keep_alive.keep_alive()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.run_polling()

if __name__ == "__main__":
    main()
