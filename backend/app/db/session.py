import sqlite3
import os
from pathlib import Path
from loguru import logger

def get_db_connection():
    """
    获取SQLite数据库连接
    
    Returns:
        sqlite3.Connection: 数据库连接对象
    """
    db_path = os.path.join("backend", "data", "xianyu_agent.db")
    db_dir = os.path.dirname(db_path)
    
    # 确保数据库目录存在
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    conn = sqlite3.connect(db_path)
    # 启用外键约束
    conn.execute("PRAGMA foreign_keys = ON")
    # 配置连接返回行为字典格式的结果
    conn.row_factory = sqlite3.Row
    
    return conn

def init_db():
    """
    初始化数据库表结构
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建消息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        item_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建索引以加速查询
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_user_item ON messages (user_id, item_id)
    ''')
    
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_timestamp ON messages (timestamp)
    ''')
    
    # 创建议价次数表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bargain_counts (
        user_id TEXT NOT NULL,
        item_id TEXT NOT NULL,
        count INTEGER DEFAULT 0,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, item_id)
    )
    ''')
    
    # 创建商品信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id TEXT PRIMARY KEY,
        data TEXT NOT NULL,
        price REAL,
        description TEXT,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("数据库初始化完成") 