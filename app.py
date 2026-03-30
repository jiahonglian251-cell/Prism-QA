import streamlit as st
import pandas as pd
from core import PrismCore

# [1] Metadata & Layout Configuration | 页面元数据与布局配置
# Restoring the wide professional layout from the original stable build.
# 恢复最初稳定版本的宽屏专业布局。
st.set_page_config(
    page_title="Prism-QA | Visual Pro Auditor",
    page_icon="💎",
    layout="wide"
)

def main():
    # --- Header Section | 界面标题栏 ---
    st.title("💎 Prism-QA Visual Pro")
    st.markdown("---")

    # --- Sidebar Configuration | 侧边栏配置 ---
    # Managing language pairs and engine status.
    # 管理语言对选择及引擎状态。
    with st.sidebar:
        st.header("⚙️ Configuration")
        src_lang = st.selectbox("Source Language | 源语言", ["Japanese", "English", "Chinese"])
        tgt_lang = st.selectbox("Target Language | 目标语言", ["Chinese", "English", "Japanese"])
        st.divider()
        st.caption("Engine: DeepSeek-V3")
        st.caption("Status: Stable v1.0.1 (Base Recovery)")
        st.info("Visual spectrum logic is active. | 可视化性能频谱已激活。")

    # --- Input Section | 文本输入区 ---
    # Dual-column layout for side-by-side text comparison.
    # 用于原文与译文对比的双栏布局。
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        source_text = st.text_area("Source Content | 原文内容", height=200, placeholder="Paste original text here...")
    with col_in2:
        target_text = st.text_area("Translated Content | 译文内容", height=200, placeholder="Paste translation here...")

    # --- Audit Execution | 审计执行逻辑 ---
    if st.button("🚀 Run Full Audit | 运行全维度审计", use_container_width=True):
        if not (source_text and target_text):
            st.warning("Validation Error: Both source and target fields are required.")
            return

        with st.spinner("DeepSeek-V3 is analyzing linguistic data..."):
            # Initializing the core audit engine.
            core = PrismCore()
            result = core.audit(source_text, target_text, src_lang, tgt_lang)
            
            if result:
                # [A] Performance Spectrum | 性能可视化渲染
                # Renders the bar chart based on scores provided by core.py.
                # 根据 core.py 提供的评分数据渲染柱状图。
                st.subheader("📊 Performance Spectrum | 性能可视化")
                scores = result.get('scores', {})
                
                if scores:
                    # Filter out 'Total' for chart visualization to focus on sub-metrics.
                    # 过滤掉“Total”键，使柱状图专注于各维度指标。
                    chart_data = {k: v for k, v in scores.items() if k != 'Total'}
                    st.bar_chart(pd.Series(chart_data))
                    
                    # Core Metric Metrics | 核心得分指标展示
                    # Specifically aligned with keys in core.py: 'Total', 'Accuracy', 'Fluency'.
                    # 严格对齐 core.py 中的键名：'Total', 'Accuracy', 'Fluency'。
                    col_s1, col_s2, col_s3 = st.columns(3)
                    col_s1.metric("Overall Score", f"{scores.get('Total', 'N/A')}/100")
                    col_s2.metric("Accuracy", f"{scores.get('Accuracy', 'N/A')}%")
                    col_s3.metric("Fluency", f"{scores.get('Fluency', 'N/A')}%")

                # [B] Deduction Details | 审计详情说明
                # Expanding deduction items with reason and location.
                # 展示包含原因与定位的扣分项详情。
                st.subheader("🚫 Deduction Details | 审计详情说明")
                deductions = result.get('deductions', [])
                if deductions:
                    for item in deductions:
                        # Aligned with 'category' and 'points' keys in core.py.
                        # 对齐 core.py 中的 'category' 和 'points' 键。
                        cat = item.get('category', 'General')
                        pts = item.get('points', '0')
                        with st.expander(f"⚠️ {cat} (-{pts} pts)"):
                            st.write(f"**Reason | 扣分原因:** {item.get('reason', 'N/A')}")
                            st.write(f"**Location | 上下文定位:** `{item.get('location', 'N/A')}`")
                else:
                    st.success("No deductions found. The translation is high quality.")

                # [C] Refined Suggestion | 优化建议译文
                # Aligned with 'refined_translation' key in core.py.
                # 严格对齐 core.py 中的 'refined_translation' 键。
                st.subheader("💡 Refined Suggestion | 优化建议译文")
                refined = result.get('refined_translation')
                if refined:
                    st.info(refined)
                    # Support for additional Chinese commentary if present.
                    # 如果存在额外的中文注释，则一并展示。
                    comment = result.get('comment_zh')
                    if comment:
                        st.caption(f"**Note:** {comment}")
                else:
                    st.warning("Suggestion engine returned empty. Check core prompt.")
            else:
                st.error("Engine Error: The backend returned an invalid response.")

if __name__ == "__main__":
    main()