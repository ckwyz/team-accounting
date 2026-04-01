import requests

# 1. 自动获取ETH实时价格（CoinGecko API）
def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usdt"
    try:
        res = requests.get(url, timeout=5)
        return res.json()["ethereum"]["usdt"]
    except:
        return 2104.24  # fallback

# 2. 合约盈亏计算函数
def eth_contract_calc(direction, entry_price, leverage, size, fee_rate=0.0004):
    current_price = get_eth_price()
    margin = (entry_price * size) / leverage
    if direction == "long":
        pnl = (current_price - entry_price) * size - (entry_price*size*0.0002 + current_price*size*0.0002)
    elif direction == "short":
        pnl = (entry_price - current_price) * size - (entry_price*size*0.0002 + current_price*size*0.0002)
    else:
        return "方向错误"
    roi = (pnl / margin) * 100
    return {
        "当前ETH价格(USDT)": round(current_price,2),
        "开仓价": entry_price,
        "杠杆": leverage,
        "持仓张数": size,
        "占用保证金(USDT)": round(margin,2),
        "未实现盈亏(USDT)": round(pnl,2),
        "收益率(%)": round(roi,2)
    }

# 3. 调用示例
result = eth_contract_calc(direction="long", entry_price=2000, leverage=20, size=5)
for k,v in result.items():
    print(f"{k}: {v}")
