import requests


class AliexpressApi:

    def __init__(self,
                 app_key,
                 app_secret,
                 language='EN',
                 currency='USD',
                 tracking_id="default",
                 ship_to='DZ'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.language = language
        self.currency = currency
        self.tracking_id = tracking_id
        self.ship_to = ship_to

    def search_by_url(self, url):
        api_url = "https://ali-api.vercel.app/api/v2/deeplink"
        params = {
            "url": url,
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "language": self.language,
            "currency": self.currency,
            "tracking_id": self.tracking_id,
            "ship_to": self.ship_to
        }

        try:
            response = requests.get(api_url, params=params)
            data = response.json()

            # التأكد من أن الاستجابة تحتوي بيانات صحيحة
            if 'title' not in data:
                raise Exception("الاستجابة غير صالحة أو ناقصة")

            return {
                "title": data.get("title"),
                "original_price": data.get("original_price"),
                "coins_price": data.get("coins_price"),
                "coins_link": data.get("coins_link"),
                "limited_offer_price": data.get("limited_offer_price"),
                "limited_offer_link": data.get("limited_offer_link"),
                "other_discount_price": data.get("other_discount_price"),
                "other_discount_link": data.get("other_discount_link"),
                "coins_discount_percentage":
                data.get("coins_discount_percentage"),
                "store_name": data.get("store_name"),
                "store_positive_rate": data.get("store_positive_rate"),
                "shipping_provider_name": data.get("shipping_provider_name"),
                "shipping_fees": data.get("shipping_fees"),
                "product_main_link": data.get("product_main_link")
            }

        except Exception as e:
            print(f"[ERROR] Failed to fetch product data: {e}")
            return None
