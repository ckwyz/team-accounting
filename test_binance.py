import requests

url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
try:
    res = requests.get(url, timeout=5)
    print(f"状态码: {res.status_code}")
    data = res.json()
    print(f"数据: {data}")
    if "price" in data:
        print(f"ETH价格: {data['price']}")
except Exception as e:
    print(f"错误: {e}")
