import asyncio
import os
from loguru import logger
from dotenv import load_dotenv

from app.xianyu_adapter.ws_client import XianyuLiveClient
from app.agent.reply_bot import XianyuReplyBot
from app.db.session import init_db


async def main():
    """
    主入口函数
    """
    # 初始化日志
    logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="00:00", level="INFO")
    
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库
    init_db()
    
    # 获取cookies
    cookies_str = os.getenv("COOKIES_STR")
    if not cookies_str:
        logger.error("环境变量中缺少COOKIES_STR配置，请检查.env文件")
        return
    
    # 创建并启动WebSocket客户端
    xianyu_client = XianyuLiveClient(cookies_str)
    
    logger.info("闲鱼自动回复系统启动成功！")
    
    # 启动WebSocket客户端
    await xianyu_client.start()


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main()) 