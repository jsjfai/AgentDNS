FROM registry.cn-jssz1.ctyun.cn/aidev/python:3.13-slim-bookworm

# 创建一个工作目录
WORKDIR /app

# 替换为阿里云的源（仅 Debian/Ubuntu）
RUN sed -i 's/http:\/\/deb.debian.org/https:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/http:\/\/security.debian.org/https:\/\/mirrors.aliyun.com\/debian-security/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y vim iputils-ping postgresql-client

# 安装Python依赖
RUN pip install --retries=5 --timeout=120 \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    mcp psycopg2-binary fastapi aiohttp

COPY ./ .

CMD ["python", "app.py"]