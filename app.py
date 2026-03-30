import streamlit as st
import pandas as pd
from fpdf import FPDF
from core import PrismCore
import io

# 页面配置
st.set_page_config(page_title="Prism-QA Visual Pro", page_icon="💎", layout="wide")

def generate_pdf(result):
    """根据审计结果生成 PDF 字节流"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Prism-QA Translation Audit Report", ln=True, align='C')
    pdf.ln(10)
    
    # 1. 核心得分
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. Overall Performance", ln=True)
    pdf.set_font("Arial", '', 11)
    scores = result.get('scores', {})
    for metric, score in scores.items():
        pdf.cell(200, 8, txt=f"- {metric}: {score}", ln=True)
    pdf.ln(5)
    
    # 2. 扣分详情
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. Deduction Details", ln=True)
    pdf.set_font("Arial", '', 10)
    for issue in result.get('deductions', []):
        text = f"[{issue.get('point', 'N/A')}] {issue.get('category', 'Error')}: {issue.get('reason', '')}"
        pdf.multi_cell(0, 8, txt=text)
    
    # 返回二进制数据
    return pdf.output(dest='S').encode('latin-1')

def main():
    st.title("💎 Prism-QA: Visual Translation Auditor")
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ Configuration")
        src_lang = st.selectbox("Source Language", ["Japanese", "English", "Chinese"])
        tgt_lang = st.selectbox("Target Language", ["Chinese", "English", "Japanese"])
        st.info("Powered by DeepSeek-V3 & Pandas")

    # 主界面输入
    col1, col2 = st.columns(2)
    with col1:
        source_text = st.text_area("Source Text (Original)", height=200)
    with col2:
        target_text = st.text_area("Target Text (Translation)", height=200)

    if st.button("🚀 Start Professional Audit"):
        if source_text and target_text:
            with st.spinner("Analyzing with DeepSeek-V3..."):
                core = PrismCore()
                result = core.audit(source_text, target_text, src_lang, tgt_lang)
                
                if result:
                    # --- 1. 显示得分统计 ---
                    st.markdown("---")
                    st.subheader("📊 Performance Spectrum")
                    scores = result.get('scores', {})
                    df = pd.DataFrame({"Metric": list(scores.keys()), "Score": list(scores.values())}).set_index("Metric")
                    if "Overall Score" in df.index:
                        df_chart = df.drop(index="Overall Score")
                        st.bar_chart(df_chart)
                    
                    # --- 2. 显示扣分详情  ---
                    st.subheader("🚫 Deduction Details")
                    for issue in result.get('deductions', []):
                        with st.expander(f"⚠️ {issue.get('point')} | {issue.get('category')}"):
                            st.write(f"**Reason:** {issue.get('reason')}")
                            st.write(f"**Location:** `{issue.get('location')}`")

                    # --- 3. 显示修改建议 ---
                    st.subheader("💡 Refined Suggestion")
                    st.info(result.get('refined_suggestion', "No suggestion available."))

                    # --- 4. 关键：下载 PDF 报告按钮 ---
                    st.markdown("---")
                    try:
                        pdf_data = generate_pdf(result)
                        st.download_button(
                            label="📥 Download PDF Audit Report",
                            data=pdf_data,
                            file_name="Prism_QA_Audit_Report.pdf",
                            mime="application/pdf"
                        )
                        st.success("Report ready for download!")
                    except Exception as e:
                        st.error(f"PDF Export Error: {e}")
                else:
                    st.error("Audit failed. Please check your API connection.")
        else:
            st.warning("Please enter both source and target text.")

if __name__ == "__main__":
    main()