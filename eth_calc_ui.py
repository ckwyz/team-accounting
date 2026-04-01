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

# 合约盈亏计算函数
def eth_contract_calc(direction, entry_price, leverage, margin_amount, current_price):
    # 根据保证金和杠杆计算实际持仓金额
    position_value = margin_amount * leverage  # 持仓金额 = 保证金 × 杠杆
    size = position_value / entry_price  # ETH数量
    
    # 实际占用保证金（考虑杠杆后）
    actual_margin = position_value / leverage
    
    if direction == "做多 (Long)":
        pnl = (current_price - entry_price) * size - (entry_price * size * 0.0002 + current_price * size * 0.0002)
    else:  # 做空
        pnl = (entry_price - current_price) * size - (entry_price * size * 0.0002 + current_price * size * 0.0002)
    
    roi = (pnl / actual_margin) * 100
    
    return {
        "size": size,
        "position_value": position_value,
        "margin": actual_margin,
        "pnl": pnl,
        "roi": roi
    }

# 页面标题
st.markdown('<h1 class="main-header">📈 ETH合约盈亏计算器</h1>', unsafe_allow_html=True)

# 获取当前ETH价格
current_eth_price = get_eth_price()

# 显示当前ETH价格
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if current_eth_price:
        st.metric("🔥 当前ETH价格 (USDT)", f"${current_eth_price:,.2f}")
    else:
        st.error("⚠️ 无法获取实时价格，请手动输入")
        current_eth_price = 2100.0

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
    
    # 开仓价 (USDT)
    entry_price = st.number_input(
        "开仓价格 (USDT)",
        min_value=0.0,
        value=2000.0,
        step=10.0,
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
    
    # 保证金金额 (USDT) - 用户输入的实际投入金额
    margin_amount = st.number_input(
        "开仓保证金 (USDT)",
        min_value=10.0,
        value=500.0,
        step=50.0,
        format="%.2f",
        help="输入你实际投入的保证金金额，系统会自动计算杠杆后的持仓金额"
    )
    
    # 当前价格（可手动调整，USDT）
    manual_price = st.number_input(
        "当前ETH价格 (USDT) - 可手动调整",
        min_value=0.0,
        value=float(current_eth_price) if current_eth_price else 2100.0,
        step=10.0,
        format="%.2f"
    )

# 计算按钮
with col_right:
    st.subheader("📊 计算结果")
    
    if st.button("🚀 计算盈亏", type="primary", use_container_width=True):
        result = eth_contract_calc(direction, entry_price, leverage, margin_amount, manual_price)
        
        # 显示结果卡片
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # 盈亏显示
        pnl_color = "profit" if result["pnl"] >= 0 else "loss"
        pnl_icon = "📈" if result["pnl"] >= 0 else "📉"
        pnl_text = "盈利" if result["pnl"] >= 0 else "亏损"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3>{pnl_icon} 未实现{pnl_text}</h3>
            <p class="{pnl_color} metric-value">${result['pnl']:,.2f} USDT</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 详细数据
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("💰 开仓保证金", f"${margin_amount:,.2f}")
            st.metric("📊 收益率", f"{result['roi']:,.2f}%", 
                     delta=f"{result['roi']:,.2f}%", 
                     delta_color="normal" if result['roi'] >= 0 else "inverse")
        
        with col_b:
            st.metric("🎯 开仓价格", f"${entry_price:,.2f}")
            st.metric("💵 当前价格", f"${manual_price:,.2f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 持仓信息
        st.markdown("---")
        st.subheader("📋 持仓信息")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"持仓数量: {result['size']:.6f} ETH")
        with col_info2:
            st.info(f"实际持仓金额: ${result['position_value']:,.2f}")
        
        # 强平价格估算（简化计算）
        st.markdown("---")
        st.subheader("⚠️ 风险提示")
        
        if direction == "做多 (Long)":
            liquidation_price = entry_price * (1 - 1/leverage + 0.005)
            st.warning(f"预估强平价格: ${liquidation_price:,.2f} USDT")
        else:
            liquidation_price = entry_price * (1 + 1/leverage - 0.005)
            st.warning(f"预估强平价格: ${liquidation_price:,.2f} USDT")
        
        # 交易详情
        with st.expander("查看详细计算"):
            st.write(f"""
            **计算详情：**
            - 交易方向: {direction}
            - 开仓价格: ${entry_price:,.2f} USDT
            - 当前价格: ${manual_price:,.2f} USDT
            - 杠杆倍数: {leverage}x
            - 开仓保证金: ${margin_amount:,.2f} USDT
            - 实际持仓金额: ${result['position_value']:,.2f} USDT (保证金 × 杠杆)
            - 持仓数量: {result['size']:.6f} ETH
            - 开仓手续费: ${entry_price * result['size'] * 0.0002:,.2f} USDT
            - 平仓手续费: ${manual_price * result['size'] * 0.0002:,.2f} USDT
            - 未实现盈亏: ${result['pnl']:,.2f} USDT
            - 收益率: {result['roi']:,.2f}%
            """)

# 底部说明
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>💡 提示：本计算器仅供参考，实际盈亏以交易所为准</p>
    <p>手续费按开仓0.02% + 平仓0.02%计算</p>
    <p>数据来源: OKX API</p>
</div>
""", unsafe_allow_html=True)
