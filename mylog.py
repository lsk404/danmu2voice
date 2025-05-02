import logging
from config import log_path
# 创建 Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置最低级别
# 控制台 Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台只显示 INFO 及以上

# 文件 Handler
file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # 文件记录 DEBUG 及以上

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 添加 Handler
logger.addHandler(console_handler)
logger.addHandler(file_handler)

