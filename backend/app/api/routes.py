from fastapi import APIRouter
from .endpoints import agents, filter, logs

# 创建主路由
api_router = APIRouter()

# 注册各模块路由
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(filter.router, prefix="/filter", tags=["filter"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"]) 