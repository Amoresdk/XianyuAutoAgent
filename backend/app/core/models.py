from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    """
    通用的API响应模型，符合项目API规范
    """
    error: int = Field(0, description="错误码: 0=正常, 500=系统异常, 401=未登录, 其他=业务异常")
    body: Dict[str, Any] = Field({}, description="业务数据对象")
    message: str = Field("", description="错误或提示信息") 