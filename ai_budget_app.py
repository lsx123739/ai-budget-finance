# ai_budget_app.py（主入口）
import streamlit as st

# 必须放在最前面！
st.set_page_config(
    page_title="AI 预算系统",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AI 智能预算编制系统")
st.subheader("请从左侧导航选择功能模块")
st.write("---")
st.info("提示：请先进入【数据上传与标准化】上传数据，再进行预算编制。")
