import streamlit as st
import pandas as pd
from core import PrismCore

# [1] Metadata & Layout | 页面元数据与布局配置
st.set_page_config(
    page_title="Prism-QA | Visual Pro Auditor",
    page_icon="💎",
    layout="wide"
)

def main():
    # --- Header | 标题栏 ---
    st.title("💎 Prism-QA Visual Pro")
    st.markdown("---")

    # --- Sidebar | 侧边栏配置 ---
    with st.sidebar:
        st.header("⚙️ Configuration")
        src_lang = st.selectbox("Source Language | 源语言", ["Japanese", "English", "Chinese"])
        tgt_lang = st.selectbox("Target Language | 目标语言", ["Chinese", "English", "Japanese"])
        
        st.divider()
        st.caption("Engine: DeepSeek-V3")
        st.caption("Status: Stable v1.0.3 (PDF-Free)")
        st.info("Visual performance spectrum is active. | 性能谱图已激活。")

    # --- Input | 文本输入区 ---
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        source_text = st.text_area("Source Content | 原文内容", height=250, placeholder="Paste original text here...")
    with col_in2:
        target_text = st.text_area("Translated Content | 译文内容", height=250, placeholder="Paste translation here...")

    # --- Logic | 核心审计逻辑 ---
    if st.button("🚀 Run Full Audit | 运行全维度审计", use_container_width=True):
        if not source_text or not target_text:
            st.warning("Validation: Please provide both source and target content.")
            return

        with st.spinner("Analyzing linguistic patterns via DeepSeek-V3..."):
            core = PrismCore()
            result = core.audit(source_text, target_text, src_lang, tgt_lang)
            
            if result:
                # [A] Visual Spectrum | 性能可视化
                st.subheader("📊 Performance Spectrum | 性能可视化")
                scores = result.get('scores', {})
                
                if scores:
                    # Renders the bar chart | 渲染柱状图
                    df = pd.DataFrame({"Metric": list(scores.keys()), "Score": list(scores.values())}).set_index("Metric")
                    if "Overall Score" in df.index:
                        st.bar_chart(df.drop(index="Overall Score"))
                    elif "overall_score" in df.index:
                        st.bar_chart(df.drop(index="overall_score"))
                    
                    # Score Metrics Display | 核心得分指标展示
                    # Robust Key-check to prevent N/A | 健壮性检查，防止出现 N/A
                    col_s1, col_s2, col_s3 = st.columns(3)
                    
                    overall = scores.get('Overall Score') or scores.get('overall_score', 'N/A')
                    accuracy = scores.get('Accuracy') or scores.get('accuracy', 'N/A')
                    fluency = scores.get('Fluency') or scores.get('fluency', 'N/A')
                    
                    col_s1.metric("Overall Score", f"{overall}/100")
                    col_s2.metric("Accuracy", f"{accuracy}%")
                    col_s3.metric("Fluency", f"{fluency}%")

                # [B] Deduction Details | 扣分诊断说明
                st.subheader("🚫 Deduction Details | 审计详情说明")
                for item in result.get('deductions', []):
                    # Using icons and color for industrial feel
                    with st.expander(f"⚠️ {item.get('category')} (-{item.get('point')} pts)"):
                        st.write(f"**Reason | 扣分原因:** {item.get('reason')}")
                        st.write(f"**Location | 上下文定位:** `{item.get('location')}`")

                # [C] Refined Suggestion | 优化建议译文
                st.subheader("💡 Refined Suggestion | 优化建议译文")
                refined = result.get('refined_suggestion', "No data provided.")
                st.info(refined)
                
            else:
                st.error("Audit Engine Error: No response from backend.")

if __name__ == "__main__":
    main()