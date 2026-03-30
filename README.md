# 💎 Prism-QA: Professional Translation Auditor (Visual Pro)

[简体中文](./README.md) | [English](./README.md)

Prism-QA 是一款基于 **DeepSeek-V3** 引擎的工业级翻译质量审计工具。它不仅能对翻译结果进行深度逻辑审计，还集成了数据可视化频谱和专业的 PDF 报告导出功能。
Prism-QA is an industrial-grade TQA tool powered by DeepSeek-V3, featuring multi-dimensional visual analytics and automated PDF report generation.

---

## ✨ 核心特性 | Key Features

* **📊 性能频谱可视化 (Visual Spectrum)**: 利用 `Pandas` 驱动图表，直观展示准确度、流利度、术语及风格得分。
* **🚫 精准扣分诊断 (Deduction Tracking)**: 自动标注扣分点、原因及原文位置，模仿人工审校深度。
* **📥 一键 PDF 导出 (Professional Export)**: 使用 `FPDF` 引擎，将审计结果转化为结构化的 PDF 报告供下载。
* **🛡️ 工业级安全性 (Security First)**: 严格通过 `.env` 隔离 API Key，确保秘钥不泄露至 GitHub。

---

## 🛠️ 技术栈 | Tech Stack

本项目采用了典型的 **AI + Data Visualization** 技术栈：

* **LLM (大语言模型)**: [DeepSeek-V3](https://www.deepseek.com/) - 负责核心的翻译逻辑审计与多维度评分。
* **Frontend (前端框架)**: [Streamlit](https://streamlit.io/) - 快速构建交互式 Web 审计面板。
* **Data Analysis (数据处理)**: [Pandas](https://pandas.pydata.org/) - 负责将 JSON 审计结果转化为 DataFrame 并驱动可视化图表。
* **Report Engine (报告引擎)**: [FPDF](http://www.fpdf.org/) - 用于生成结构化的专业 PDF 审计报告。
* **Security (安全管理)**: [Python-dotenv](https://pypi.org/project/python-dotenv/) - 确保 API Key 等敏感信息通过环境变量隔离。

---

## 🚀 快速开始 | Quick Start

### 1. 安装依赖 | Install Dependencies
在终端运行以下命令：
```bash
pip install streamlit pandas fpdf python-dotenv requests

### 2. 环境配置 | Configuration
请在根目录手动创建 .env 文件，并填入以下内容：
```bash
DEEPSEEK_API_KEY=你的_DEEPSEEK_实际密钥
USE_PROXY=True

### 3. 启动应用 | Launch Dashboard
终端内输入以下以运行：
```bash
streamlit run app.py
