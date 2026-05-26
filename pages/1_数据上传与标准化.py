import streamlit as st
import pandas as pd

st.title("📂 数据上传与标准化")

uploaded_file = st.file_uploader("上传 Excel/CSV 财务数据", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    
    st.session_state.df_clean = df
    st.success("✅ 数据清洗完成，字段标准化成功")
    st.dataframe(df, use_container_width=True)
else:
    st.info("请上传 Excel 或 CSV 文件")
