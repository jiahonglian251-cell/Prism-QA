import os
import requests
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# [ZH] 初始化环境与日志 [EN] Initialize environment and logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PrismCore:
    """
    [ZH] 工业级翻译审计核心，支持多维度评分与可视化数据输出
    [EN] Industrial-grade translation audit core, supporting multi-dimensional scoring and visual data output
    """
    def __init__(self):
        self.api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url: str = "https://api.deepseek.com/v1"
        # [ZH] 代理配置：根据 .env 中的 USE_PROXY 决定是否启用 [EN] Proxy config: Toggle based on USE_PROXY in .env
        self.proxies: Optional[Dict[str, str]] = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        } if os.getenv("USE_PROXY") == "True" else None

    def _get_system_prompt(self) -> str:
        # [ZH] 核心提示词：定义严格的 JSON 结构，包含得分点与扣分项 
        # [EN] Core prompt: Define strict JSON structure with scores and deductions
        return (
            "You are a professional TQA auditor. Analyze the translation and return ONLY a JSON object: "
            "{"
            "  'scores': {'Accuracy': 0-100, 'Fluency': 0-100, 'Terminology': 0-100, 'Style': 0-100, 'Total': 0-100},"
            "  'deductions': [{'category': '...', 'points': int, 'reason': '...', 'location': '...'}],"
            "  'refined_translation': '...',"
            "  'comment_zh': '...'"
            "}"
        )

    def audit(self, source: str, target: str, src_lang: str, tgt_lang: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": f"Source ({src_lang}): {source}\nTarget ({tgt_lang}): {target}"}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2  # [ZH] 降低随机性以确保审计一致性 [EN] Lower temperature for consistency
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload, proxies=self.proxies, timeout=30)
            response.raise_for_status()
            return json.loads(response.json()['choices'][0]['message']['content'])
        except Exception as e:
            logging.error(f"Audit failed: {e}")
            return {"error": str(e)}