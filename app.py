from mcp.server.fastmcp import FastMCP
import asyncio
import re
import threading
from aiohttp import web
import aiohttp
import json
from urllib.parse import parse_qs

from log import logger
from auth import verify_userid_and_apikey
from agent import get_tools_number
from database import get_db_connection, init_db
from config import get_metric_baseurl, get_api_baseurl
# 邮箱格式验证正则（符合RFC标准的简化版）
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PROXY_PATHS = [
    "/api/{path:.*}",  # 代理所有 /api 开头的路径
]

mcp = FastMCP("CategoryServer", host="0.0.0.0", port=8000)

@mcp.tool()
async def category_list(userid: str="unknown", apikey: str="unset") -> dict:
    """Using a Large Language Model (LLM) to classify user questions involves leveraging the powerful language understanding and generation capabilities of LLMs. LLMs have a deep understanding of context, language structure, and semantics, allowing them to analyze the content of user questions and categorize them into predefined classes."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if verify_userid_and_apikey(userid, apikey):
                # 验证通过，查询default和当前用户的分类
                cur.execute(
                    "SELECT category, userid FROM categories WHERE userid IN ('default', %s) ORDER BY CASE WHEN userid = 'default' THEN 0 ELSE 1 END",
                    (userid,)
                )
            else:
                # 验证失败，仅查询default分类
                cur.execute(
                    "SELECT category, userid FROM categories WHERE userid = 'default' ORDER BY id"
                )
            
            result = cur.fetchall()
            # 转换为{category: userid}字典（注意处理重复category的情况）
            category_dict = {}
            for item in result:
                # 数据库行数据通常是元组，按查询字段顺序取值
                category = item["category"]
                category_dict[category] = item["userid"]
            
            return category_dict
    
    except Exception as e:
        # 异常时返回包含错误信息的字典（保持返回类型一致）
        return {"error": f"获取标签列表失败: {str(e)}"}
    
    finally:
        conn.close()

@mcp.tool()
async def category_query(category: str, userid: str="unknown", apikey: str="unset") -> dict:
    """The classification of the user's question has been identified. Look up the service address corresponding to this classification."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if verify_userid_and_apikey(userid, apikey):
                cur.execute("SELECT baseurl FROM categories WHERE category = %s AND userid IN (%s, 'default') ORDER BY CASE WHEN userid = %s THEN 0 ELSE 1 END", (category, userid, userid,))
            else:
                cur.execute("SELECT baseurl FROM categories WHERE category = %s AND userid IN ('default')", (category,))
            result = cur.fetchone()
            if result:
                baseurl = result['baseurl']
                # 更新metrics表中对应记录的called字段加1
                cur.execute("UPDATE metrics SET called = called + 1, updated_at = CURRENT_TIMESTAMP WHERE nodebaseurl = %s", (get_metric_baseurl(baseurl),))
                conn.commit()  # 提交事务
                logger.info(f"查询分类「{category}」成功，已更新metrics表中called计数")
                return {"name":category, "baseurl":baseurl}
            
            # 如果未找到，获取所有可用标签
            cur.execute("SELECT category FROM categories")
            categories = [item['category'] for item in cur.fetchall()]
            return {"name":category, "baseurl":None, "error":f"未找到category「{category}」，当前支持的category：{', '.join(categories)}"}
    except Exception as e:
        logger.error(f"查询分类时出错: {str(e)}", exc_info=True)
        return {"name":category, "baseurl":None, "error":f"查询标签失败: {str(e)}"}
    finally:
        conn.close()

@mcp.tool()
async def category_add(category: str, baseurl: str, userid: str, apikey: str) -> str:
    """You can call to add categories for user questions at any time, but we currently only support one category."""
    if not verify_userid_and_apikey(userid, apikey):
        return "错误：API Key验证失败"
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # 检查标签是否已存在
            cur.execute("SELECT id FROM categories WHERE category = %s and userid = %s", (category, userid,))
            if cur.fetchone():
                return f"错误：category「{category}」已存在，无法重复添加"
            
            # 添加新标签
            cur.execute(
                "INSERT INTO categories (category, baseurl, userid) VALUES (%s, %s, %s) RETURNING id",
                (category, baseurl, userid)
            )
            new_id = cur.fetchone()['id']
            
            # 获取当前总数
            cur.execute("SELECT COUNT(*) FROM categories")
            count = cur.fetchone()['count']
            
            # 检查baseurl是否已存在
            cur.execute("SELECT id FROM metrics WHERE nodebaseurl = %s", (baseurl,))
            if not cur.fetchone():
                # 向metrics表中添加新记录，使networkNodes增加1
                cur.execute(
                    "INSERT INTO metrics (nodebaseurl, registered_tools, available, called) VALUES (%s, %s, %s, %s)",
                    (baseurl, 0, False, 0)  # 初始化registered_tools为0，available为False，called为0
                )
                logger.info(f"成功向metrics表添加记录，对应baseurl: {baseurl}")
            else:
                logger.info(f"baseurl「{baseurl}」已存在于metrics表中，无需重复添加")
            
            return f"成功添加category「{category}」，id为：{new_id}，当前共有{count}条数据"
    except Exception as e:
        conn.rollback()
        return f"添加标签失败: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
async def category_delete(category: str, userid: str, apikey: str) -> str:
    """It can be called at any time to delete question categories, and similarly, only first-level categories are supported at present."""
    if not verify_userid_and_apikey(userid, apikey):
        return "错误：API Key验证失败"
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # 检查标签是否存在
            cur.execute("SELECT id, baseurl FROM categories WHERE category = %s AND userid = %s", (category, userid,))
            result = cur.fetchone()
            if not result:
                # 获取所有可用标签
                cur.execute("SELECT category FROM categories")
                categories = [item['category'] for item in cur.fetchall()]
                return f"错误：未找到category「{category}」，当前支持的category：{', '.join(categories)}"
            
            # 获取对应的baseurl
            baseurl = result['baseurl']
            
            # 判断categories中是否存在多个相同的baseurl
            cur.execute("SELECT COUNT(*) FROM categories WHERE baseurl = %s", (baseurl,))
            count = cur.fetchone()['count']
            if count > 1:
                logger.warning(f"categories中存在多个category对应baseurl「{baseurl}」，跳过删除metrics记录")
            else:
                # 从metrics表中删除对应的记录，使networkNodes减1
                cur.execute("DELETE FROM metrics WHERE nodebaseurl = %s", (baseurl,))
                deleted_count = cur.rowcount  # 获取删除的记录数
                logger.info(f"从metrics表中删除{deleted_count}条记录，对应baseurl: {baseurl}")
            
            # 删除标签
            cur.execute("DELETE FROM categories WHERE category = %s AND userid = %s", (category, userid,))

            # 获取剩余数量
            cur.execute("SELECT COUNT(*) FROM categories")
            count = cur.fetchone()['count']
            
            return f"成功删除category「{category}」，当前剩余{count}条数据"
    except Exception as e:
        conn.rollback()
        return f"删除标签失败: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
async def register_user(userid: str, apikey: str) -> str:
    """Use email as userid and self generated apikey to register."""
    if not EMAIL_PATTERN.match(userid):
        return f"Invalid userid"
    
    if len(apikey) < 6:
        return f"Then lenth of apikey should not smaller than 6"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # 检查标签是否已存在
            cur.execute("SELECT id FROM users WHERE userid = %s", (userid,))
            if cur.fetchone():
                # 用户存在，更新密码
                cur.execute("UPDATE users SET passwd = %s WHERE userid = %s",(apikey, userid))
                return f"Updated apikey to {apikey}"
            else:
                # 添加新用户
                cur.execute(
                    "INSERT INTO users (userid, passwd) VALUES (%s, %s)",
                    (userid, apikey)
                )
                return f"Remember your userid {userid} and apikey {apikey}"
    except Exception as e:
        conn.rollback()
        return f"添加用户失败: {str(e)}"
    finally:
        conn.close()

async def get_metrics(request):
    # 因为run_metrics_cron_job现在是异步函数，需要用await调用
    await run_metrics_cron_job()
    
    retVal = {
        "success": False,
        "data": {
            "networkNodes": 0,
            "registeredAgents": 0,
            "availability": 0,
            "called": 0
        }
    }
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM metrics ORDER BY id")
            result = cur.fetchall()
            logger.debug(f"获取metrics成功: {result}")
            retVal["success"] = True
            retVal["data"]["networkNodes"] = len(result)
            available_nodes = 0
            for item in result:
                retVal["data"]["registeredAgents"] += item["registered_tools"]
                if item["available"]:
                    available_nodes += 1
                retVal["data"]["called"] += item["called"]
            if retVal["data"]["networkNodes"] > 0:  # 避免除零错误
                percentage = available_nodes / retVal["data"]["networkNodes"] * 100
                retVal["data"]["availability"] = f"{percentage:.2f}%"
            else:
                retVal["data"]["availability"] = "0.00%"
    except Exception as e:
        logger.error(f"获取metrics失败: {str(e)}")
    finally:
        conn.close()
        return web.json_response(retVal)  # 确保返回aiohttp的响应对象

async def run_metrics_cron_job():
    """
    定时任务：每分钟更新metrics表中available字段
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM metrics ORDER BY id")
            result = cur.fetchall()
            need_commit = False
            for item in result:
                if not item["nodebaseurl"].endswith('$smart'):
                    continue
                baseurl = item["nodebaseurl"].split("$smart")[0].rstrip("/")
                registered_tools = await asyncio.create_task(get_tools_number(baseurl))
                
                if registered_tools == item["registered_tools"]:
                    continue
                need_commit = True
                available = registered_tools > 0
                cur.execute("UPDATE metrics SET registered_tools = %s, available = %s WHERE id = %s", 
                           (registered_tools, available, item['id']))
                logger.info(f"更新metrics表中记录，id: {item['id']}, registered_tools: {registered_tools}, available: {available}")
            if need_commit:
                conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"更新metrics表失败: {str(e)}", exc_info=True)
    finally:
        conn.close()

async def proxy_handler(request):
    original_path = request.path
    original_query = request.query_string
    query_params = parse_qs(original_query)
    category = query_params.get("category", ["unset"])[0]
    userid = query_params.get("userid", ["unset"])[0]
    apikey = query_params.get("apikey", ["unset"])[0]
    category_result = await category_query(category, userid, apikey)
    baseurl = category_result["baseurl"]
    if not baseurl:
        return web.Response(
            text=json.dumps({"error": "category not found"}, indent=2),
            status=400,
            content_type="application/json"
        )
    api_baseurl = get_api_baseurl(baseurl)
    logger.info(f"api_baseurl: {api_baseurl}")
    backend_url = f"{api_baseurl}{original_path}"

    # 处理查询参数
    query_string = request.query_string
    if query_string:
        backend_url += f"?{query_string}"
    
    # 复制请求头（过滤不需要转发的头）
    headers = {}
    for k, v in request.headers.items():
        if k.lower() not in ("host", "connection", "content-length"):
            headers[k] = v
    
    # 转发请求到后端
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=request.method,
                url=backend_url,
                headers=headers,
                data=await request.read(),
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                return web.Response(
                    body=await response.read(),
                    status=response.status,
                    headers=response.headers
                )
    except Exception as e:
        return web.Response(
            text=json.dumps({"error": f"Proxy failed: {str(e)}"}, indent=2),
            status=502,
            content_type="application/json"
        )

def setup_routes(app):
    # 配置 RESTful API 路由
    app.router.add_get("/metrics", get_metrics)
    for path in PROXY_PATHS:
        app.router.add_route("*", path, proxy_handler)

def run_rest_api():
    """单独的线程函数：启动REST API服务"""
    app = web.Application()
    setup_routes(app)
    web.run_app(app, host="0.0.0.0", port=8080) 

def run_mcp_server():
    mcp.run(transport="sse")

if __name__ == "__main__":
    # 初始化数据库
    init_db()

    # 启动MCP服务器（主线程）
    mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
    mcp_thread.start()
    logger.info("MCP服务已在 http://0.0.0.0:8000 启动")

    # 创建并启动REST API线程
    logger.info("REST API服务已在 http://0.0.0.0:8080 启动")
    run_rest_api()