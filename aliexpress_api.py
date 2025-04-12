import requests
from models import ProductInfo

class AliexpressApi:
    def init(self, app_key: str, tracking_id: str):
        self.app_key = app_key
        self.tracking_id = tracking_id

    def get_product_by_url(self, url: str) -> ProductInfo:
        try:
            res = requests.get(
                "https://ali-link.vercel.app/api",
                params={"url": url}
            )
            data = res.json()
            return ProductInfo(
                title=data.get("title", "No Title"),
                price=data.get("price", "N/A"),
                link=data.get("link", url),
                image=data.get("image", "")
            )
        except Exception as e:
            print(f"[ERROR] Failed to get product info: {e}")
            return None
