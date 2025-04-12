
import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re
import urllib.parse
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from keep_alive import keep_alive

bot = telebot.TeleBot('8193262941:AAF1P-o_LISQfl-PYiU26tBTk8jaIaqQVFs')  # استبدل بالتوكن الخاص بك
ADMIN_ID = 5412967206

# إعداد AliExpress API
aliexpress = AliexpressApi(
    '514130',
    'nV8vFBa61NIsLcx2KOgJjoRByzmIfnO0',
    language=models.Language.EN,
    currency=models.Currency.USD,
    tracking_id='default'
)

# كيبورد الاشتراك
keyboardStart = types.InlineKeyboardMarkup(row_width=1)
subscribe_button = types.InlineKeyboardButton("❤️ اشترك في القناة", url="https://t.me/Red_Store0")
keyboardStart.add(subscribe_button)

# أمر /start
@bot.message_handler(commands=['start'])
def welcome_user(message):
    bot.send_message(
        message.chat.id,
        "مرحباً بك، أرسل لنا رابط المنتج الذي تريد شراءه لنوفر لك أفضل سعر له",
        reply_markup=keyboardStart
    )

# أوامر عرض وتحميل السجل
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

            keyboard = types.InlineKeyboardMarkup()
            download_button = types.InlineKeyboardButton("📥 تحميل السجل", callback_data="download_again")
            keyboard.add(download_button)

            bot.send_message(message.chat.id, "يمكنك تحميل السجل من الزر أيضاً:", reply_markup=keyboard)
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

# استخراج أول رابط من النص
def extract_link(text):
    match = re.search(r'https?://[^\s]+', text)
    return match.group() if match else None

# جلب معلومات المنتج
def get_product_info(link, chat_id):
    try:
        affiliate_links = aliexpress.get_affiliate_links(link)
        product_info = aliexpress.get_products_details([link])
        if product_info:
            product = product_info[0]
            title = product.product_title
            image = product.product_main_image_url
            price = product.target.sale_price

            caption = f"""المنتج: {title}
السعر: {price} USD
♻️ العرض باستخدام النقاط والكوبونات متاح
رابط الشراء: {affiliate_links[0].promotion_link}
#AliXPromotion ✅"""

            bot.send_photo(chat_id, image, caption=caption)
        else:
            bot.send_message(chat_id, "لم يتم العثور على تفاصيل المنتج.")
    except Exception as e:
        print(e)
        bot.send_message(chat_id, "حدث خطأ أثناء جلب بيانات المنتج.")

# استقبال جميع الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or "بدون اسم"
    full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
    text = message.text
    chat_id = message.chat.id
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"[{timestamp}] {full_name} | @{username} | ID: {user_id} | ChatID: {chat_id}:\n{text}\n\n"
{text}

    print(log_line)
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(log_line)

    link = extract_link(text)
    if link:
        get_product_info(link, chat_id)

keep_alive()
bot.infinity_polling()
