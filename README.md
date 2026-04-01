# ETH合约盈亏计算器

一个基于Streamlit的ETH合约盈亏计算Web应用，支持人民币计价。

## 功能特性

- 📈 实时获取ETH价格（OKX API）
- 💱 自动获取USD/CNY汇率
- 🇨🇳 全人民币计价（开仓价格、持仓金额、盈亏）
- 📊 支持做多/做空双向计算
- ⚠️ 强平价格预警
- 💰 手续费计算（开仓0.02% + 平仓0.02%）

## 使用方法

1. 输入开仓价格（人民币）
2. 选择杠杆倍数
3. 输入持仓金额（人民币）
4. 调整当前ETH价格（可选）
5. 点击"计算盈亏"查看结果

## 在线访问

部署在 Streamlit Community Cloud: [你的应用链接]

## 本地运行

```bash
pip install -r requirements.txt
streamlit run eth_calc_ui.py
```

## 技术栈

- Python 3.8+
- Streamlit
- Requests
