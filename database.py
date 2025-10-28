import os
import psycopg2
from psycopg2.extras import RealDictCursor

from log import logger

# 数据库连接配置 - 建议通过环境变量或配置文件管理
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "category_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "192.168.201.180"),
    "port": os.getenv("DB_PORT", "30432")
}

# 初始化数据库连接
def get_db_connection():
    """创建并返回数据库连接"""
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            cursor_factory=RealDictCursor
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        logger.error(f"数据库连接错误: {e}")
        raise

# 初始化数据库表
def init_db():
    """初始化数据库表结构"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # 创建categories表
            cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                category VARCHAR(256) NOT NULL,
                userid VARCHAR(256) NOT NULL DEFAULT 'default',
                baseurl TEXT NOT NULL
            )
            """)
            # 创建metrics表
            cur.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id                SERIAL        PRIMARY KEY,
                nodebaseurl       TEXT          NOT NULL,
                registered_tools  INT           NOT NULL    DEFAULT 0,
                available         BOOLEAN       NOT NULL    DEFAULT False,
                called            INT           NOT NULL    DEFAULT 0,
                updated_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
            )
            """)
            # 创建users表
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id                SERIAL        PRIMARY KEY,
                userid            VARCHAR(256)  NOT NULL    UNIQUE,
                passwd            VARCHAR(256)  NOT NULL
            )
            """)
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化错误: {e}")
        conn.rollback()
    finally:
        conn.close()
