import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from config import TARGET_TIMEZONE
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # 配置日志文件
    log_file = "/var/log/app.log"
    if os.name == 'nt':
        log_file = "./app.log"
    handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",  # 每天午夜分割日志文件
        interval=1,
        backupCount=7  # 保留 7 天的日志文件
    )

    # 自定义 Formatter 类
    class TzFormatter(logging.Formatter):
        def __init__(self, fmt=None, datefmt=None, tz=ZoneInfo('UTC')):
            super().__init__(fmt, datefmt)
            self.tz = tz

        def formatTime(self, record, datefmt=None):
            dt = datetime.fromtimestamp(record.created, self.tz)
            if datefmt:
                s = dt.strftime(datefmt)
            else:
                s = dt.isoformat()
            return s

    # 定义日志格式
    formatter = TzFormatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S', TARGET_TIMEZONE)
    handler.setFormatter(formatter)

    # 创建日志记录器
    logger.addHandler(handler)
    return logger

logger = setup_logger()