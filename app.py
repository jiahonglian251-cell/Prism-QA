import streamlit as st
import pandas as pd
from core import PrismCore
import os

# [1] System Configuration | 系统环境配置
# Ensuring a clean, wide professional layout
# 确保整洁、宽屏的专业布局
st.set_page_config(
    page_title="Prism-QA | Pro Translation Auditor",
    page_icon="💎",
    layout="wide"
)

def main():
    # --- UI Header | 界面标题 ---
    st.title("💎 Prism-QA Visual Pro")
    st.markdown("---")

    # --- Sidebar Configuration | 侧边栏配置 ---
    with st.sidebar:
        st.header("⚙️ Configuration")
        # Language selection for the audit engine
        # 为审计引擎选择语言对
        src_lang = st.selectbox("Source Language | 源语言", ["Japanese", "English", "Chinese"])
        tgt_lang = st.selectbox("Target Language | 目标语言", ["Chinese", "English", "Japanese"])
        
        st.divider()
        # Displaying engine and environment status
        # 展示引擎及环境状态
        st.caption("Engine: DeepSeek-V3")
        st.caption("Environment: Stable v1.0.2 (PDF Disabled)")
        st.info("Visual Spectrum & Logic Audit: Active")

    # --- Input Section | 文本输入区 ---
    # Using two-column layout for side-by-side comparison
    # 使用两栏布局进行原文/译文对比
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        source_text = st.text_area("Source Content | 原文内容", height=250, placeholder="Paste original text here...")
    with col_in2:
        target_text = st.text_area("Translated Content | 译文内容", height=250, placeholder="Paste translation here...")

    # --- Execution Logic | 审计执行逻辑 ---
    if st.button("🚀 Run Full Audit | 运行全维度审计", use_container_width=True):
        if not source_text or not target_text:
            st.warning("Input required: Both fields must be filled.")
            return

        with st.spinner("DeepSeek-V3 is analyzing linguistic patterns..."):
            # Initialize core logic from core.py
            # 初始化 core.py 中的核心逻辑
            core = PrismCore()
            result = core.audit(source_text, target_text, src_lang, tgt_lang)
            
            if result:
                # [A] Visual Spectrum | 性能可视化
                # Renders a professional bar chart based on scores
                # 根据得分渲染专业柱状图
                st.subheader("📊 Performance Spectrum | 性能可视化")
                scores = result.get('scores', {})
                if scores:
                    # Convert score dict to DataFrame for visualization
                    df = pd.DataFrame({"Metric": list(scores.keys()), "Score": list(scores.values())}).set_index("Metric")
                    if "Overall Score" in df.index:
                        # Chart focus: sub-metrics only
                        st.bar_chart(df.drop(index="Overall Score"))
                    
                    # Display numerical summary
                    # 展示数值摘要
                    col_score1, col_score2, col_score3 = st.columns(3)
                    col_score1.metric("Overall Score", f"{scores.get('Overall Score', 'N/A')}/100")
                    col_score2.metric("Accuracy", f"{scores.get('Accuracy', 'N/A')}%")
                    col_score3.metric("Fluency", f"{scores.get('Fluency', 'N/A')}%")

                # [B] Detailed Diagnostics | 详细审计诊断
                # Using expanders to keep the UI clean
                # 使用折叠框保持界面整洁
                st.subheader("🚫 Audit Diagnostics | 审计详情说明")
                deductions = result.get('deductions', [])
                if deductions:
                    for item in deductions:
                        with st.expander(f"⚠️ {item.get('category')} (-{item.get('point')} pts)"):
                            st.write(f"**Reason | 扣分原因:** {item.get('reason')}")
                            st.write(f"**Context | 上下文定位:** `{item.get('location')}`")
                else:
                    st.success("Perfect alignment detected! No deductions found.")

                # [C] Refined Output | 优化建议译文
                # Showing the AI-improved version of the text
                # 展示 AI 优化后的建议译文
                st.subheader("💡 Refined Suggestion | 优化建议译文")
                refined = result.get('refined_suggestion', "No suggestion provided.")
                st.info(refined)

            else:
                st.error("Audit Engine returned an empty result. Check API connectivity.")

if __name__ == "__main__":
    main()