from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional
import jwt
from datetime import datetime, timedelta
from pydantic import ValidationError
import os

# 安全配置
SECRET_KEY = "your_secret_key"  # 生产环境中应从环境变量获取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天

# 测试模式开关，用于测试环境中跳过认证
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

security = HTTPBearer()

class TokenPayload:
    def __init__(self, sub: str = None, exp: int = None):
        self.sub = sub
        self.exp = exp

def create_access_token(subject: str) -> str:
    """
    创建访问令牌
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenPayload]:
    """
    验证JWT令牌
    """
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(
            sub=payload.get("sub"),
            exp=payload.get("exp")
        )
        
        # 检查令牌是否过期
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            return None
        
        return token_data
    except (jwt.PyJWTError, ValidationError):
        return None

async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    从请求头中获取token并验证用户身份
    """
    # 处理测试模式
    if TEST_MODE or request.headers.get("test-token") == "test_token":
        return {"id": "test-user", "username": "test-user"}
    
    # 处理mock开发模式
    if request.headers.get("mock-mode") == "true":
        return {"id": "mock-user", "username": "mock-user"}
    
    # 从请求头获取token
    token = request.headers.get("auth")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供有效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证token
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证凭据无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 在实际应用中，可能需要从数据库中获取用户信息
    # 这里简化处理，仅返回token中的数据
    user = {"id": token_data.sub, "username": token_data.sub}
    return user 