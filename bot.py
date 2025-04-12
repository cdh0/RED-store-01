
import telebot
from telebot import types
from datetime import datetime
from keep_alive import keep_alive
from aliexpress_api import AliexpressApi, models

bot = telebot.TeleBot('8193262941:AAF1P-o_LISQfl-PYiU26tBTk8jaIaqQVFs')
ADMIN_ID = 5412967206

# AliExpress API config
aliexpress = AliexpressApi(
    '514130',
    'nV8vFBa61NIsLcx2KOgJjoRByzmIfnO0',
    language=models.Language.EN,
    currency=models.Currency.USD,
    tracking_id='default'
)

@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    subscribe_button = types.InlineKeyboardButton("❤️ اشترك في القناة", url="https://t.me/Red_Store0")
    keyboard.add(subscribe_button)
    bot.send_message(message.chat.id, "مرحباً بك، أرسل لنا رابط المنتج الذي تريد شراءه لنوفر لك أفضل سعر له", reply_markup=keyboard)

@bot.message_handler(commands=["logs"])
def send_logs(message):
    if message.chat.id == ADMIN_ID:
        try:
            with open("logs.txt", "r", encoding="utf-8") as f:
                logs = f.readlines()
            last_logs = logs[-30:]
            bot.send_message(message.chat.id, "".join(last_logs))
            keyboard = types.InlineKeyboardMarkup()
            download_button = types.InlineKeyboardButton("📥 تحميل السجل", callback_data="download_again")
            keyboard.add(download_button)
            bot.send_message(message.chat.id, "يمكنك تحميل السجل الكامل من الزر أدناه:", reply_markup=keyboard)
        except Exception as e:
            bot.send_message(message.chat.id, f"خطأ: {e}")
    else:
        bot.send_message(message.chat.id, "ماعندكش صلاحية.")

@bot.message_handler(commands=["download"])
def send_log_file(message):
    if message.chat.id == ADMIN_ID:
        try:
            with open("logs.txt", "rb") as f:
                bot.send_document(message.chat.id, f)
        except Exception as e:
            bot.send_message(message.chat.id, f"خطأ: {e}")
    else:
        bot.send_message(message.chat.id, "ماعندكش صلاحية.")

@bot.callback_query_handler(func=lambda call: call.data == "download_again")
def resend_log_file(call):
    if call.message.chat.id == ADMIN_ID:
        try:
            with open("logs.txt", "rb") as f:
                bot.send_document(call.message.chat.id, f)
        except:
            bot.send_message(call.message.chat.id, "حدث خطأ أثناء إرسال الملف.")

def get_product_info(link, chat_id):
    try:
        bot.send_message(chat_id, "⏳ يتم الآن معالجة الرابط...")

        affiliate_links = aliexpress.get_affiliate_links(link)
        product_info = aliexpress.get_products_details([link])

        if product_info:
            product = product_info[0]
            title = product.product_title
            image = product.product_main_image_url
            current_price = product.original_price
            coins_price = getattr(product, 'coins_price', 'غير متوفر')
            limited_offer_price = getattr(product, 'limited_offer_price', 'غير متوفر')
            other_discount_price = getattr(product, 'other_discount_price', 'غير متوفر')
            coins_discount_percentage = getattr(product, 'coins_discount_percentage', 'غير متوفر')
            store_name = getattr(product, 'store_name', 'غير متوفر')
            store_positive_rate = getattr(product, 'store_positive_rate', 'غير متوفر')
            shipping_provider_name = getattr(product, 'shipping_provider_name', 'غير متوفر')
            shipping_fees = getattr(product, 'shipping_fees', 'غير متوفر')

            coins_link = affiliate_links[0].promotion_link
            limited_offer_link = affiliate_links[0].promotion_link
            other_discount_link = affiliate_links[0].promotion_link

            caption = f"""🔥 تخفيض ل {title}

🟡 سعر المنتج بدون تخفيض : {current_price}$
{coins_link}

🟡 سعر التخفيض بالعملات : {coins_price}$
{coins_link}

🟡 سعر العرض المحدود : {limited_offer_price}$
{limited_offer_link}

🟡 سعر التخفيض المحتمل : {other_discount_price}$
{other_discount_link}

💯 نسبة التخفيض بالعملات : {coins_discount_percentage}%
🏪 إسم المتجر : {store_name}
🌟 التقييم الإيجابي للمتجر : {store_positive_rate}
✈️ شركة الشحن : {shipping_provider_name}
✈️ عمولة الشحن : {shipping_fees}$
"""
            bot.send_photo(chat_id, image, caption=caption)
        else:
            bot.send_message(chat_id, "❌ لم يتم العثور على تفاصيل المنتج.")
    except Exception as e:
        print(e)
        bot.send_message(chat_id, "❌ حدث خطأ أثناء جلب بيانات المنتج.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or "بدون اسم"
    full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    text = message.text
    chat_id = message.chat.id
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {full_name} | @{username} | ID: {user_id} | ChatID: {chat_id}:
{text}

"
    print(log_line)
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(log_line)

    if "aliexpress.com" in text or "s.click.aliexpress.com" in text:
        get_product_info(text, chat_id)

keep_alive()
bot.infinity_polling()
