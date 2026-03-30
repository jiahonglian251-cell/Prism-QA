import streamlit as st
import pandas as pd
from fpdf import FPDF
from core import PrismCore
import os

def generate_pdf_report(result):
    """
    Industrial-grade PDF generator: Fixed for Chinese rendering space issues.
    工业级 PDF 生成器：修复中文渲染空间不足的问题。
    """
    from fpdf import FPDF
    
    # 1. 显式设置边距，确保有足够空间
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(left=15, top=15, right=15) 
    pdf.add_page()
    
    font_path = os.path.join("fonts", "SimSun.ttf")
    
    if os.path.exists(font_path):
        try:
            pdf.add_font('ChineseMain', '', font_path)
            pdf.set_font('ChineseMain', '', 14)
        except Exception as e:
            st.error(f"Font Error: {e}")
            pdf.set_font("Arial", 'B', 16)
    
    # --- 标题写入 ---
    pdf.cell(w=0, h=10, txt="Prism-QA 翻译审计报告", ln=True, align='C')
    pdf.ln(10)

    # --- 核心内容写入 (关键改动：使用 w=0 和更稳健的 multi_cell) ---
    pdf.set_font('ChineseMain', '', 12) if os.path.exists(font_path) else pdf.set_font("Arial", '', 12)
    
    # 写入得分
    pdf.cell(w=0, h=10, txt="[1] 评分统计 (Performance Scores):", ln=True)
    scores = result.get('scores', {})
    for metric, score in scores.items():
        pdf.cell(w=0, h=8, txt=f"- {metric}: {score}", ln=True)
    
    pdf.ln(5)
    
    # 写入诊断细节
    pdf.cell(w=0, h=10, txt="[2] 扣分诊断 (Diagnostics):", ln=True)
    for item in result.get('deductions', []):
        reason_text = f"• [{item.get('category')}] 扣{item.get('point')}分: {item.get('reason')}"
        # 关键：multi_cell 的 w=0 代表使用当前边距到右边距的全部宽度
        pdf.multi_cell(w=0, h=8, txt=reason_text)
        pdf.ln(2)

    return pdf.output()

def main():
    st.set_page_config(page_title="Prism-QA Visual Pro", layout="wide")
    st.title("💎 Prism-QA Visual Pro")
    
    # 侧边栏与输入逻辑 (保持之前的工业级双语设置)
    with st.sidebar:
        st.header("⚙️ Configuration")
        src_lang = st.selectbox("Source Language", ["Japanese", "English", "Chinese"])
        tgt_lang = st.selectbox("Target Language", ["Chinese", "English", "Japanese"])

    source_text = st.text_area("Source Text", height=200)
    target_text = st.text_area("Target Text", height=200)

    if st.button("🚀 Run Full Audit | 运行全维度审计", use_container_width=True):
        if source_text and target_text:
            with st.spinner("Processing..."):
                core = PrismCore()
                result = core.audit(source_text, target_text, src_lang, tgt_lang)
                
                if result:
                    # A. 可视化图表
                    st.subheader("📊 Performance Spectrum | 性能可视化")
                    scores = result.get('scores', {})
                    df = pd.DataFrame({"Metric": list(scores.keys()), "Score": list(scores.values())}).set_index("Metric")
                    if "Overall Score" in df.index:
                        st.bar_chart(df.drop(index="Overall Score"))
                    
                    # B. 扣分详情
                    st.subheader("🚫 Audit Diagnostics | 审计详情")
                    for item in result.get('deductions', []):
                        with st.expander(f"⚠️ {item.get('category')} (-{item.get('point')} pts)"):
                            st.write(f"**Reason:** {item.get('reason')}")

                    # C. 报告导出 (关键下载入口)
                    st.divider()
                    try:
                        pdf_data = generate_pdf_report(result)
                        st.download_button(
                            label="📥 Download Professional PDF Report (Support Chinese)",
                            data=bytes(pdf_data),
                            file_name="Prism_QA_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"PDF Output Error: {e}")
                else:
                    st.error("Audit Engine Error.")

if __name__ == "__main__":
    main()