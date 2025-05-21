from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import api_router
import os
from loguru import logger
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建应用实例
app = FastAPI(
    title="闲鱼AutoAgent API",
    description="闲鱼自动代理系统API接口",
    version="1.0.0"
)

# 配置日志
logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="00:00", level="INFO")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应限制为实际前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "闲鱼AutoAgent API服务已启动"}

# 在生产环境中，你可能需要在这里初始化Sentry或其他监控工具
# if os.getenv("ENVIRONMENT") == "production":
#     import sentry_sdk
#     sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))

# 导入所有API路由
# 当创建了API路由后取消注释以下代码
# from app.api.endpoints import conversations, settings, system

# 包含API路由
# app.include_router(conversations.router)
# app.include_router(settings.router)
# app.include_router(system.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 