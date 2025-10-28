import os

from log import logger
from database import get_db_connection

def get_valid_api_keys_from_configmap():
    """从ConfigMap读取合法的API Key列表"""
    try:
        api_keys_str = os.getenv("API_KEYS", "")
        if not api_keys_str:
            raise ValueError("ConfigMap中未配置API_KEYS")
        return [key.strip() for key in api_keys_str.split(",") if key.strip()]
    except Exception as e:
        raise RuntimeError(f"读取ConfigMap失败: {str(e)}")

def verify_api_key(request_api_key: str) -> bool:
    """验证请求中的API Key是否在ConfigMap的合法列表中"""
    if not request_api_key:
        return False
    valid_keys = get_valid_api_keys_from_configmap()
    return request_api_key in valid_keys

def verify_userid_and_apikey(userid: str, apikey: str) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            sql = "SELECT userid FROM users WHERE userid = %s AND passwd = %s"
            cur.execute(sql, (userid, apikey,))
            row = cur.fetchone()
            return bool(row)
    except Exception as e:
        logger.error(e)
        return False
    finally:
        conn.close()
