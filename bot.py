import telebot
from telebot import types
from aliexpress_api import AliexpressApi, models
import re
import urllib.parse
import json
from urllib.parse import urlparse, parse_qs
from keep_alive import keep_alive

bot = telebot.TeleBot('8193262941:AAF1P-o_LISQfl-PYiU26tBTk8jaIaqQVFs')

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

            # عرض المنتج للمستخدم
            caption = f"""🛍 المنتج: {title}
💵 السعر: {price} USD
♻️ العرض باستخدام النقاط والكوبونات متاح
🔗 رابط الشراء: {affiliate_links[0].promotion_link}
#AliXPromotion ✅"""

            bot.send_photo(chat_id, image, caption=caption)
        else:
            bot.send_message(chat_id, "لم يتم العثور على تفاصيل المنتج.")

    except Exception as e:
        print(e)
        bot.send_message(chat_id, "حدث خطأ أثناء جلب بيانات المنتج.")

# التعامل مع أي رابط
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    link = extract_link(message.text)
    if link and "aliexpress.com" in link:
        bot.send_message(message.chat.id, "⏳ يتم الآن معالجة الرابط...")
        get_product_info(link, message.chat.id)
    else:
        bot.send_message(message.chat.id, "الرجاء إرسال رابط منتج صحيح من AliExpress.")

# تشغيل السيرفر على Replit
keep_alive()

# تشغيل البوت
bot.infinity_polling()
