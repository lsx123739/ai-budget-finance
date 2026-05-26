import streamlit as st
import pandas as pd

st.title("🧠 智能预算编制模块")

# 防报错：检查数据是否已上传
if "df_clean" not in st.session_state or st.session_state.df_clean is None:
    st.error("⚠️ 请先在「数据上传与标准化」上传数据！")
    st.stop()

df = st.session_state.df_clean

# 预算参数设置
period = st.selectbox("预算周期", ["月度", "季度", "年度"])
grow_rate = st.number_input("收入增长率(%)", value=10)
cost_rate = st.number_input("成本占收入比(%)", value=60)
fee_rate = st.number_input("费用上限占收入比(%)", value=15)

if st.button("AI生成预算方案"):
    # 计算基础收入（取金额列的总和）
    base_revenue = df.iloc[:, 1].sum()
    budget_revenue = base_revenue * (1 + grow_rate / 100)
    budget_cost = budget_revenue * (cost_rate / 100)
    budget_fee = budget_revenue * (fee_rate / 100)
    budget_profit = budget_revenue - budget_cost - budget_fee

    st.subheader("📊 预算结果")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("预算收入", round(budget_revenue, 2))
    col2.metric("预算成本", round(budget_cost, 2))
    col3.metric("预算费用", round(budget_fee, 2))
    col4.metric("预计利润", round(budget_profit, 2))
