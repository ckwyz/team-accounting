import requests

url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usdt"
try:
    res = requests.get(url, timeout=5)
    print(f"状态码: {res.status_code}")
    print(f"响应内容: {res.text}")
    data = res.json()
    print(f"解析后的数据: {data}")
    if "ethereum" in data:
        print(f"ETH数据: {data['ethereum']}")
        if "usdt" in data["ethereum"]:
            print(f"ETH价格: {data['ethereum']['usdt']}")
        else:
            print("usdt字段不存在")
    else:
        print("ethereum字段不存在")
except Exception as e:
    print(f"错误: {e}")
