from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
from pydantic import BaseModel

from ...core.models import ResponseModel
from ...services.agent_service import AgentService
from ...core.security import get_current_user

router = APIRouter()

# 定义请求模型
class ToggleAgentStatusRequest(BaseModel):
    agent_type: str
    enabled: bool

class UpdateAgentPromptRequest(BaseModel):
    agent_type: str
    prompt: str

class AgentSettingsModel(BaseModel):
    enabled: bool
    prompt: str

class SaveAllAgentSettingsRequest(BaseModel):
    agents: Dict[str, AgentSettingsModel]

@router.post("/settings", response_model=ResponseModel)
async def get_agent_settings(
    request: Dict[str, Any] = {},
    current_user: Dict[str, Any] = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """
    获取所有Agent的设置信息
    """
    try:
        agents = agent_service.get_all_agent_settings()
        return {
            "error": 0,
            "body": {"agents": agents},
            "message": ""
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"获取Agent设置失败: {str(e)}"
        }

@router.post("/toggle-status", response_model=ResponseModel)
async def toggle_agent_status(
    request: ToggleAgentStatusRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """
    更新Agent的启用状态
    """
    try:
        agent_type = request.agent_type
        enabled = request.enabled
        
        # 检查agent_type是否有效
        valid_types = ["intent", "sales", "tech", "price"]
        if agent_type not in valid_types:
            return {
                "error": 400,
                "body": {},
                "message": f"无效的Agent类型: {agent_type}"
            }
        
        # 更新状态
        agent_service.update_agent_status(agent_type, enabled)
        
        return {
            "error": 0,
            "body": {"success": True},
            "message": ""
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"更新Agent状态失败: {str(e)}"
        }

@router.post("/update-prompt", response_model=ResponseModel)
async def update_agent_prompt(
    request: UpdateAgentPromptRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """
    更新Agent的提示词
    """
    try:
        agent_type = request.agent_type
        prompt = request.prompt
        
        # 检查agent_type是否有效
        valid_types = ["intent", "sales", "tech", "price"]
        if agent_type not in valid_types:
            return {
                "error": 400,
                "body": {},
                "message": f"无效的Agent类型: {agent_type}"
            }
        
        # 检查提示词是否为空
        if not prompt or prompt.strip() == "":
            return {
                "error": 400,
                "body": {},
                "message": "提示词不能为空"
            }
        
        # 更新提示词
        agent_service.update_agent_prompt(agent_type, prompt)
        
        return {
            "error": 0,
            "body": {"success": True},
            "message": ""
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"更新Agent提示词失败: {str(e)}"
        }

@router.post("/save-all-settings", response_model=ResponseModel)
async def save_all_agent_settings(
    request: SaveAllAgentSettingsRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    agent_service: AgentService = Depends()
):
    """
    保存所有Agent的设置
    """
    try:
        agents_config = request.agents
        
        # 检查所有必需的Agent类型是否都存在
        required_types = ["intent", "sales", "tech", "price"]
        for agent_type in required_types:
            if agent_type not in agents_config:
                return {
                    "error": 400,
                    "body": {},
                    "message": f"缺少必需的Agent类型: {agent_type}"
                }
        
        # 保存所有设置
        agent_service.save_all_agent_settings(agents_config)
        
        return {
            "error": 0,
            "body": {"success": True},
            "message": ""
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"保存Agent设置失败: {str(e)}"
        } 