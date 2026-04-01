import streamlit as st
import requests

# 页面配置
st.set_page_config(
    page_title="ETH合约盈亏计算器",
    page_icon="📈",
    layout="wide"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .profit {
        color: #28a745;
        font-weight: bold;
    }
    .loss {
        color: #dc3545;
        font-weight: bold;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 获取ETH实时价格 (USDT)
@st.cache_data(ttl=60)
def get_eth_price():
    try:
        url = "https://www.okx.com/api/v5/market/ticker?instId=ETH-USDT"
        res = requests.get(url, timeout=5)
        data = res.json()
        if data.get("code") == "0" and data.get("data"):
            return float(data["data"][0]["last"])
    except:
        pass
    return None

# 获取USD/CNY汇率
@st.cache_data(ttl=300)
def get_usd_cny_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        res = requests.get(url, timeout=5)
        data = res.json()
        return float(data["rates"]["CNY"])
    except:
        pass
    
    # 备用汇率
    try:
        url = "https://www.okx.com/api/v5/market/ticker?instId=USDC-CNY"
        res = requests.get(url, timeout=5)
        data = res.json()
        if data.get("code") == "0" and data.get("data"):
            return float(data["data"][0]["last"])
    except:
        pass
    
    return 7.2  # 默认汇率

# 合约盈亏计算函数
def eth_contract_calc(direction, entry_price_usdt, leverage, position_value_cny, current_price_usdt, usd_cny_rate):
    # 将持仓人民币价值转换为ETH数量
    entry_price_cny = entry_price_usdt * usd_cny_rate
    size = position_value_cny / entry_price_cny  # ETH数量
    
    margin = (entry_price_usdt * size) / leverage
    margin_cny = margin * usd_cny_rate
    
    if direction == "做多 (Long)":
        pnl_usdt = (current_price_usdt - entry_price_usdt) * size - (entry_price_usdt * size * 0.0002 + current_price_usdt * size * 0.0002)
    else:  # 做空
        pnl_usdt = (entry_price_usdt - current_price_usdt) * size - (entry_price_usdt * size * 0.0002 + current_price_usdt * size * 0.0002)
    
    pnl_cny = pnl_usdt * usd_cny_rate
    roi = (pnl_usdt / margin) * 100
    
    return {
        "size": size,
        "margin_usdt": margin,
        "margin_cny": margin_cny,
        "pnl_usdt": pnl_usdt,
        "pnl_cny": pnl_cny,
        "roi": roi
    }

# 页面标题
st.markdown('<h1 class="main-header">📈 ETH合约盈亏计算器</h1>', unsafe_allow_html=True)

# 获取当前价格和汇率
current_eth_price = get_eth_price()
usd_cny_rate = get_usd_cny_rate()

# 显示当前价格信息
col1, col2, col3 = st.columns(3)
with col1:
    if current_eth_price:
        st.metric("🔥 ETH价格", f"${current_eth_price:,.2f}")
    else:
        st.error("⚠️ 无法获取ETH价格")
        current_eth_price = 2100.0

with col2:
    st.metric("💱 USD/CNY汇率", f"¥{usd_cny_rate:.2f}")

with col3:
    if current_eth_price:
        eth_price_cny = current_eth_price * usd_cny_rate
        st.metric("🇨🇳 ETH价格", f"¥{eth_price_cny:,.2f}")

st.markdown("---")

# 输入区域
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚙️ 交易参数设置")
    
    # 方向选择
    direction = st.radio(
        "交易方向",
        ["做多 (Long)", "做空 (Short)"],
        horizontal=True
    )
    
    # 开仓价 (人民币)
    entry_price_cny = st.number_input(
        "开仓价格 (CNY ¥)",
        min_value=0.0,
        value=15000.0,
        step=100.0,
        format="%.2f"
    )
    
    # 杠杆倍数
    leverage = st.slider(
        "杠杆倍数",
        min_value=1,
        max_value=125,
        value=20,
        step=1
    )
    
    # 持仓金额 (人民币)
    position_value_cny = st.number_input(
        "持仓金额 (CNY ¥)",
        min_value=100.0,
        value=10000.0,
        step=1000.0,
        format="%.2f",
        help="输入你想要投入的人民币金额"
    )
    
    # 当前价格（可手动调整，人民币）
    if current_eth_price:
        default_price_cny = current_eth_price * usd_cny_rate
    else:
        default_price_cny = 15120.0
    
    manual_price_cny = st.number_input(
        "当前ETH价格 (CNY ¥) - 可手动调整",
        min_value=0.0,
        value=default_price_cny,
        step=100.0,
        format="%.2f"
    )

# 计算按钮
with col_right:
    st.subheader("📊 计算结果")
    
    if st.button("🚀 计算盈亏", type="primary", use_container_width=True):
        # 转换为USDT价格进行计算
        entry_price_usdt = entry_price_cny / usd_cny_rate
        manual_price_usdt = manual_price_cny / usd_cny_rate
        
        result = eth_contract_calc(direction, entry_price_usdt, leverage, position_value_cny, manual_price_usdt, usd_cny_rate)
        
        # 显示结果卡片
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # 盈亏显示
        pnl_color = "profit" if result["pnl_cny"] >= 0 else "loss"
        pnl_icon = "📈" if result["pnl_cny"] >= 0 else "📉"
        pnl_text = "盈利" if result["pnl_cny"] >= 0 else "亏损"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3>{pnl_icon} 未实现{pnl_text}</h3>
            <p class="{pnl_color} metric-value">¥{result['pnl_cny']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 详细数据
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("💰 占用保证金", f"¥{result['margin_cny']:,.2f}")
            st.metric("📊 收益率", f"{result['roi']:,.2f}%", 
                     delta=f"{result['roi']:,.2f}%", 
                     delta_color="normal" if result['roi'] >= 0 else "inverse")
        
        with col_b:
            st.metric("🎯 开仓价格", f"¥{entry_price_cny:,.2f}")
            st.metric("💵 当前价格", f"¥{manual_price_cny:,.2f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 持仓信息
        st.markdown("---")
        st.subheader("📋 持仓信息")
        st.info(f"持仓数量: {result['size']:.6f} ETH")
        
        # 强平价格估算（简化计算）
        st.markdown("---")
        st.subheader("⚠️ 风险提示")
        
        if direction == "做多 (Long)":
            liquidation_price_usdt = entry_price_usdt * (1 - 1/leverage + 0.005)
            liquidation_price_cny = liquidation_price_usdt * usd_cny_rate
            st.warning(f"预估强平价格: ¥{liquidation_price_cny:,.2f}")
        else:
            liquidation_price_usdt = entry_price_usdt * (1 + 1/leverage - 0.005)
            liquidation_price_cny = liquidation_price_usdt * usd_cny_rate
            st.warning(f"预估强平价格: ¥{liquidation_price_cny:,.2f}")
        
        # 交易详情
        with st.expander("查看详细计算"):
            st.write(f"""
            **计算详情：**
            - 交易方向: {direction}
            - 开仓价格: ¥{entry_price_cny:,.2f} (${entry_price_usdt:,.2f})
            - 当前价格: ¥{manual_price_cny:,.2f} (${manual_price_usdt:,.2f})
            - 杠杆倍数: {leverage}x
            - 持仓金额: ¥{position_value_cny:,.2f}
            - 持仓数量: {result['size']:.6f} ETH
            - 占用保证金: ¥{result['margin_cny']:,.2f} (${result['margin_usdt']:,.2f})
            - 开仓手续费: ${entry_price_usdt * result['size'] * 0.0002:,.2f} USDT
            - 平仓手续费: ${manual_price_usdt * result['size'] * 0.0002:,.2f} USDT
            - 未实现盈亏: ¥{result['pnl_cny']:,.2f} (${result['pnl_usdt']:,.2f})
            - 收益率: {result['roi']:,.2f}%
            - USD/CNY汇率: {usd_cny_rate:.2f}
            """)

# 底部说明
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>💡 提示：本计算器仅供参考，实际盈亏以交易所为准</p>
    <p>手续费按开仓0.02% + 平仓0.02%计算</p>
    <p>数据来源: OKX API / Exchange Rate API</p>
</div>
""", unsafe_allow_html=True)
