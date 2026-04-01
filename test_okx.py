import requests

# OKX API
url = "https://www.okx.com/api/v5/market/ticker?instId=ETH-USDT"
try:
    res = requests.get(url, timeout=5)
    print(f"状态码: {res.status_code}")
    data = res.json()
    print(f"数据: {data}")
    if data.get("code") == "0" and data.get("data"):
        print(f"ETH价格: {data['data'][0]['last']}")
except Exception as e:
    print(f"错误: {e}")
