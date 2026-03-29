import sqlite3
import logging
import json
from datetime import datetime

# --- Logger Configuration ---
# [EN] Standard logging for tracking database events.
# [ZH] 标准化日志，用于追踪数据库事件。
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db(db_name: str = "prism_qa.db"):
    """
    [EN] Initializes the database schema for storing audit records.
    [ZH] 初始化用于存储审计记录的数据库架构。
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang VARCHAR(10),
                    target_lang VARCHAR(10),
                    total_score REAL,
                    detail_json TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.info(f"Database consistency check passed: {db_name}")
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")

def save_audit_result(source, target, s_lang, t_lang, result_dict, db_name="prism_qa.db"):
    """
    [EN] Persists the Agent's JSON output into the SQLite database.
    [ZH] 将 Agent 的 JSON 输出持久化到 SQLite 数据库中。
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_records 
                (source_text, translated_text, source_lang, target_lang, total_score, detail_json)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (source, target, s_lang, t_lang, result_dict['scores']['total'], json.dumps(result_dict)))
            conn.commit()
            logging.info("Audit record successfully persisted to local storage.")
    except Exception as e:
        logging.error(f"Failed to save record: {e}")

# Footnote: Using 'with' statement ensures connection is closed automatically.
# 脚注：使用 'with' 语句确保连接在操作后自动关闭。