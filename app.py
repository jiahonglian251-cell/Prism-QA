import streamlit as st
import pandas as pd
from core import PrismCore

# [ZH] 页面高级配置 [EN] Page high-level configuration
st.set_page_config(page_title="Prism-QA Visual Pro", page_icon="💎", layout="wide")

def main():
    st.title("💎 Prism-QA: Visual Audit Dashboard")
    st.markdown("---")

    # [ZH] 侧边栏设置 [EN] Sidebar settings
    with st.sidebar:
        st.header("⚙️ Configuration")
        src_lang = st.selectbox("Source Language", ["Chinese", "English", "Japanese"])
        tgt_lang = st.selectbox("Target Language", ["English", "Chinese", "Japanese"])
        st.divider()
        st.caption("Powered by DeepSeek-V3 & Pandas")

    # [ZH] 输入区域 [EN] Input area
    col_in_1, col_in_2 = st.columns(2)
    source_text = col_in_1.text_area("Source Text", height=150)
    target_text = col_in_2.text_area("Translated Text", height=150)

    if st.button("🚀 Run Visual Spectrum Audit", use_container_width=True):
        if source_text and target_text:
            worker = PrismCore()
            with st.spinner("Analyzing linguistic dimensions..."):
                result = worker.audit(source_text, target_text, src_lang, tgt_lang)
            
            if "error" in result:
                st.error(f"Audit Interrupted: {result['error']}")
            else:
                render_visuals(result)
        else:
            st.warning("Please provide both source and target texts.")

def render_visuals(data):
    """[ZH] 处理可视化逻辑 [EN] Handle visualization logic"""
    st.success("✅ Audit Completed Successfully")

    # --- [ZH] 1. 得分频谱可视化 (The Visual Scoreboard) ---
    st.subheader("📊 Performance Spectrum")
    scores = data.get('scores', {})
    
    # [ZH] 构造 Pandas 数据框用于绘图 [EN] Construct Pandas DataFrame for plotting
    df = pd.DataFrame({
        "Dimension": list(scores.keys()),
        "Score": list(scores.values())
    }).set_index("Dimension")
    
    # [ZH] 过滤掉 Total 分数以显示纯维度对比 [EN] Filter Total for pure dimension comparison
    df_plot = df.drop(index="Total") if "Total" in df.index else df
    st.bar_chart(df_plot)

    # --- [ZH] 2. 关键指标卡片 [EN] Key Metrics Cards ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Overall Score", f"{scores.get('Total', 0)}/100")
    c2.metric("Accuracy", f"{scores.get('Accuracy', 0)}%")
    c3.metric("Fluency", f"{scores.get('Fluency', 0)}%")

    # --- [ZH] 3. 详细扣分项 (Deduction Breakdown) ---
    st.subheader("🚫 Deduction Details")
    deductions = data.get('deductions', [])
    if not deductions:
        st.info("No significant errors found. Excellent translation!")
    else:
        for item in deductions:
            with st.expander(f"⚠️ -{item.get('points')} pts | {item.get('category')}"):
                st.write(f"**Reason:** {item.get('reason')}")
                st.write(f"**Location:** `{item.get('location')}`")

    # --- [ZH] 4. 优化建议 [EN] Refined Translation ---
    st.divider()
    st.subheader("💡 Refined Suggestion")
    st.info(data.get('refined_translation', ""))
    st.caption(data.get('comment_zh', ""))

if __name__ == "__main__":
    main()

from fpdf import FPDF
import io

def generate_pdf(data):
    """[ZH] 将审计结果转换为 PDF 字节流 [EN] Convert audit results to PDF byte stream"""
    pdf = FPDF()
    pdf.add_page()
    
    # [ZH] 设置标题 [EN] Set Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Prism-QA Audit Report", ln=True, align='C')
    pdf.ln(10)

    # [ZH] 写入得分 [EN] Write Scores
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. Performance Scores", ln=True)
    pdf.set_font("Arial", '', 11)
    for k, v in data.get('scores', {}).items():
        pdf.cell(200, 8, txt=f"- {k}: {v}", ln=True)
    pdf.ln(5)

    # [ZH] 写入改进建议 [EN] Write Refinement
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. Refined Suggestion", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, txt=data.get('refined_translation', ''))
    
    # [ZH] 返回字节流供 Streamlit 下载 [EN] Return bytes for Streamlit download
    return pdf.output(dest='S').encode('latin-1')

# --- 在 render_visuals 函数的末尾添加以下代码 ---
# [ZH] 添加下载按钮 [EN] Add download button
def render_visuals(data):
    # ... 原有的可视化代码 ...
    
    st.divider()
    pdf_bytes = generate_pdf(data)
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="Prism_QA_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )