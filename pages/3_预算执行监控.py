import streamlit as st

st.title("📊 预算执行监控模块")

if "df_clean" not in st.session_state:
    st.error("⚠️ 请先上传数据并生成预算！")
    st.stop()

st.subheader("实际数据录入")
real_revenue = st.number_input("实际收入")
real_cost = st.number_input("实际成本")
real_fee = st.number_input("实际费用")

if st.button("计算预算偏差"):
    # 这里用简单示例，实际可以和预算结果对比
    budget_revenue = st.session_state.get("budget_revenue", 0)
    revenue_diff = real_revenue - budget_revenue

    st.subheader("偏差分析结果")
    st.metric("收入偏差", revenue_diff)
    if revenue_diff > 0:
        st.success("✅ 收入超出预算")
    elif revenue_diff < 0:
        st.warning("⚠️ 收入未达预算")
    else:
        st.info("收入与预算持平")
