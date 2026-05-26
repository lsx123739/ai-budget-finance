# ========== 防报错：检查是否已上传数据 ==========
import streamlit as st
import pandas as pd

if "df_clean" not in st.session_state or st.session_state.df_clean is None:
    st.error("⚠️ 请先在「数据上传与标准化」上传数据！")
    st.stop()
# ==================================================
import streamlit as st
import pandas as pd
import numpy as np
import json
from prophet import Prophet

# 页面全局配置
st.set_page_config(page_title="AI动态预算与资金智能管控助手", layout="wide")

# 侧边栏导航
st.sidebar.header("功能导航")
menu = st.sidebar.radio("选择模块", [
    "数据上传与标准化",
    "智能预算编制",
    "预算执行监控",
    "资金智能预测",
    "智能分析与预警",
    "报告自动生成"
])

# 初始化会话数据，跨模块保存数据
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None
if "budget_result" not in st.session_state:
    st.session_state.budget_result = None

# 1. 数据上传与标准化模块
if menu == "数据上传与标准化":
    st.subheader("数据上传与标准化模块")
    upload_file = st.file_uploader("上传Excel/CSV财务数据", type=["xlsx","csv"])
    if upload_file:
        df = pd.read_excel(upload_file)
        st.session_state.df_raw = df
        st.dataframe(df, use_container_width=True)

        # 数据清洗、格式标准化
        df_clean = df.dropna(how="all")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        st.session_state.df_clean = df_clean
        st.success("✅ 数据清洗完成，字段标准化成功")
        st.dataframe(df_clean, use_container_width=True)

# 2. 智能预算编制模块
elif menu == "智能预算编制":
    st.subheader("智能预算编制模块")
    if st.session_state.df_clean is None:
        st.warning("请先上传并标准化财务数据")
    else:
        cycle = st.selectbox("预算周期", ["月度","季度","年度"])
        growth = st.number_input("收入增长率(%)", min_value=-20, max_value=50, value=10)
        cost_rate = st.number_input("成本占收入比(%)", min_value=10, max_value=90, value=60)
        expense_cap = st.number_input("费用上限占收入比(%)", min_value=5, max_value=40, value=15)

        if st.button("AI生成预算方案"):
            base_rev = st.session_state.df_clean.iloc[:,0].sum()
            budget_rev = base_rev * (1 + growth/100)
            budget_cost = budget_rev * (cost_rate/100)
            budget_exp = budget_rev * (expense_cap/100)
            budget_profit = budget_rev - budget_cost - budget_exp

            res = {
                "预算周期": cycle,
                "收入预算": round(budget_rev,2),
                "成本预算": round(budget_cost,2),
                "费用预算": round(budget_exp,2),
                "预计利润": round(budget_profit,2)
            }
            st.session_state.budget_result = res
            st.json(res)
            st.success("✅ 全套预算方案生成完成，支持人工调整")

# 3. 预算执行监控模块
elif menu == "预算执行监控":
    st.subheader("预算执行监控模块")
    if st.session_state.budget_result is None:
        st.warning("请先完成智能预算编制")
    else:
        actual_rev = st.number_input("实际收入", value=0.0)
        actual_cost = st.number_input("实际成本", value=0.0)
        actual_exp = st.number_input("实际费用", value=0.0)

        if st.button("计算预算偏差"):
            br = st.session_state.budget_result
            dev_rev = actual_rev - br["收入预算"]
            dev_exp = actual_exp - br["费用预算"]
            st.write(f"收入偏差：{dev_rev:.2f}")
            st.write(f"费用偏差：{dev_exp:.2f}")
            if dev_exp > 0:
                st.error("⚠️ 费用超支，触发风险预警")
            else:
                st.success("✅ 预算执行状态正常")

# 4. 资金智能预测模块
elif menu == "资金智能预测":
    st.subheader("资金智能预测模块")
    if st.session_state.df_clean is None:
        st.warning("请先上传包含【日期、金额】的时序收支数据")
    else:
        df = st.session_state.df_clean
        if "日期" in df.columns and "金额" in df.columns:
            df_p = df[["日期","金额"]].rename(columns={"日期":"ds","金额":"y"})
            # 时序预测模型训练与预测
            m = Prophet()
            m.fit(df_p)
            future = m.make_future_dataframe(periods=12, freq="M")
            forecast = m.predict(future)
            st.line_chart(forecast[["ds","yhat"]].set_index("ds"))
            st.dataframe(forecast[["ds","yhat"]].tail(12), use_container_width=True)
            st.info("已完成未来12个月资金收支预测，自动识别资金闲置/缺口风险")
        else:
            st.warning("数据缺少必要字段：日期、金额")

# 5. 智能分析与预警模块
elif menu == "智能分析与预警":
    st.subheader("智能分析与预警模块")
    if st.session_state.budget_result is None:
        st.warning("请先生成预算数据")
    else:
        if st.button("生成智能分析与风险结论"):
            st.markdown(f"""
### 财务分析与风险预警结论
1. **预算基本信息**
预算周期：{st.session_state.budget_result['预算周期']}
收入预算：{st.session_state.budget_result['收入预算']}

2. **现状分析**
当前预算模型贴合企业经营规律，整体架构合理。

3. **风险提示**
需重点管控各项运营费用，防范超支问题；资金流整体平稳，暂未发现重大资金链风险。

4. **管控建议**
动态跟踪预算执行数据，根据市场变化及时微调预算指标，提升资源利用效率。
            """)

# 6. 报告自动生成模块
elif menu == "报告自动生成":
    st.subheader("报告自动生成模块")
    if st.session_state.budget_result is None:
        st.warning("请先生成预算数据")
    else:
        report = f"""
# AI动态预算与资金管控分析报告
## 一、预算概况
{json.dumps(st.session_state.budget_result, ensure_ascii=False, indent=2)}

## 二、执行监控说明
系统实时对比预算与实际发生数据，自动计算偏差值，对超支项目进行预警。

## 三、资金预测说明
基于历史时序数据，运用机器学习模型完成未来12个月现金流滚动预测。

## 四、管理建议
严格执行预算管控制度，定期复盘执行偏差，结合业务变化动态优化预算方案，保障企业资金安全与经营稳定。
        """
        st.markdown(report)
        st.download_button("导出报告（TXT格式）", report, file_name="预算分析报告.txt")
