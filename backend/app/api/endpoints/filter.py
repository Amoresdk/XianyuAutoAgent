from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from ...core.models import ResponseModel
from ...services.filter_service import FilterService
from ...core.security import get_current_user

router = APIRouter()

# 定义请求模型
class WordRequest(BaseModel):
    word: str

# API端点：获取所有敏感词
@router.post("/words", response_model=ResponseModel)
async def get_filter_words(
    request: Dict[str, Any] = {},
    current_user: Dict[str, Any] = Depends(get_current_user),
    filter_service: FilterService = Depends()
):
    """
    获取所有已配置的敏感词
    """
    try:
        words = filter_service.get_all_words()
        return {
            "error": 0,
            "body": {
                "words": words,
                "total": len(words)
            },
            "message": ""
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"获取敏感词列表失败: {str(e)}"
        }

# API端点：添加敏感词
@router.post("/add", response_model=ResponseModel)
async def add_filter_word(
    request: WordRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    filter_service: FilterService = Depends()
):
    """
    添加新的敏感词
    """
    try:
        word = request.word
        
        # 验证敏感词非空
        if not word or word.strip() == "":
            return {
                "error": 400,
                "body": {},
                "message": "敏感词不能为空"
            }
        
        # 检查敏感词是否已存在
        if filter_service.word_exists(word):
            return {
                "error": 400,
                "body": {},
                "message": "该敏感词已存在"
            }
        
        # 添加敏感词
        filter_service.add_word(word)
        
        return {
            "error": 0,
            "body": {"success": True},
            "message": "敏感词添加成功"
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"添加敏感词失败: {str(e)}"
        }

# API端点：删除敏感词
@router.post("/delete", response_model=ResponseModel)
async def delete_filter_word(
    request: WordRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    filter_service: FilterService = Depends()
):
    """
    删除指定的敏感词
    """
    try:
        word = request.word
        
        # 验证敏感词非空
        if not word or word.strip() == "":
            return {
                "error": 400,
                "body": {},
                "message": "敏感词不能为空"
            }
        
        # 检查敏感词是否存在
        if not filter_service.word_exists(word):
            return {
                "error": 404,
                "body": {},
                "message": "该敏感词不存在"
            }
        
        # 删除敏感词
        filter_service.delete_word(word)
        
        return {
            "error": 0,
            "body": {"success": True},
            "message": "敏感词删除成功"
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"删除敏感词失败: {str(e)}"
        }

# API端点：清空敏感词
@router.post("/clear", response_model=ResponseModel)
async def clear_filter_words(
    request: Dict[str, Any] = {},
    current_user: Dict[str, Any] = Depends(get_current_user),
    filter_service: FilterService = Depends()
):
    """
    清空所有敏感词
    """
    try:
        # 清空敏感词
        filter_service.clear_all_words()
        
        return {
            "error": 0,
            "body": {"success": True},
            "message": "敏感词列表已清空"
        }
    except Exception as e:
        return {
            "error": 500,
            "body": {},
            "message": f"清空敏感词列表失败: {str(e)}"
        } 