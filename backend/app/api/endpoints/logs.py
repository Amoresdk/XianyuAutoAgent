from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from ...core.models import ResponseModel
from ...services.logs_service import LogsService
from ...core.security import get_current_user

router = APIRouter()

# 定义请求模型
class LogsRequest(BaseModel):
    line_count: Optional[int] = 100  # 默认获取100行日志

# API端点：获取最新日志
@router.post("/latest", response_model=ResponseModel)
async def get_latest_logs(
    request: LogsRequest = LogsRequest(),
    current_user: Dict[str, Any] = Depends(get_current_user),
    logs_service: LogsService = Depends()
):
    """
    获取系统最新日志
    """
    try:
        # 尝试从实际日志文件读取日志
        logs = logs_service.read_latest_log_lines(request.line_count)
        
        # 如果没有日志，使用示例日志（用于开发环境）
        if not logs or (len(logs) == 1 and "没有找到日志文件" in logs[0]):
            logs = logs_service.get_dummy_logs()
        
        return {
            "error": 0,
            "body": {"logs": logs},
            "message": ""
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"获取最新日志失败: {str(e)}"
        }

# API端点：获取错误日志
@router.post("/errors", response_model=ResponseModel)
async def get_error_logs(
    request: LogsRequest = LogsRequest(),
    current_user: Dict[str, Any] = Depends(get_current_user),
    logs_service: LogsService = Depends()
):
    """
    获取系统错误日志
    """
    try:
        # 尝试从实际日志文件读取错误日志
        logs = logs_service.read_error_log_lines(request.line_count)
        
        # 如果没有日志，使用示例错误日志（用于开发环境）
        if not logs or (len(logs) == 1 and "没有找到" in logs[0]):
            logs = logs_service.get_dummy_error_logs()
        
        return {
            "error": 0,
            "body": {"logs": logs},
            "message": ""
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"获取错误日志失败: {str(e)}"
        } 