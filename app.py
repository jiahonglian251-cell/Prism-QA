import streamlit as st
import pandas as pd
from fpdf import FPDF
from core import PrismCore
import os

def generate_pdf_report(result):
    """
    Industrial-grade PDF Generator with Unicode Injection.
    集成 Unicode 注入的工业级 PDF 生成器。
    """
    pdf = FPDF()
    pdf.add_page()
    
    # [关键] 动态路径检查与字体注册
    font_path = os.path.join("fonts", "SimSun.ttf")
    
    if os.path.exists(font_path):
        try:
            # 注册中文字体：指定别名为 'ChineseMain'
            pdf.add_font('ChineseMain', '', font_path)
            pdf.set_font('ChineseMain', '', 14)
        except Exception as e:
            st.error(f"Font loading error: {e}")
            pdf.set_font("Arial", 'B', 16)
    else:
        # 路径缺失时的 fallback 提示
        st.warning(f"Font asset missing at {font_path}. Using standard Arial.")
        pdf.set_font("Arial", 'B', 16)

    # --- 开始写入内容 ---
    pdf.cell(0, 10, txt="Prism-QA Translation Audit Report | 翻译审计报告", ln=True, align='C')
    pdf.ln(10)

    # 1. Scores | 评分
    pdf.set_font('ChineseMain' if os.path.exists(font_path) else 'Arial', '', 12)
    scores = result.get('scores', {})
    pdf.cell(0, 10, txt="Performance Scores | 评分统计:", ln=True)
    for metric, score in scores.items():
        pdf.cell(0, 8, txt=f"- {metric}: {score}", ln=True)

    # 2. Deductions | 扣分诊断
    pdf.ln(5)
    pdf.cell(0, 10, txt="Deduction Diagnostics | 扣分诊断细节:", ln=True)
    for item in result.get('deductions', []):
        # 工业级多行文本处理
        reason_text = f"[{item.get('category')}] -{item.get('point')}pts: {item.get('reason')}"
        pdf.multi_cell(0, 8, txt=reason_text)

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