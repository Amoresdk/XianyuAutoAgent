import pytest
from fastapi.testclient import TestClient
import json
import os
from pathlib import Path

# 导入FastAPI应用
from backend.app.main import app

# 创建测试客户端
client = TestClient(app)

# 测试数据
TEST_TOKEN = "test_token"
HEADERS = {"auth": TEST_TOKEN, "Content-Type": "application/json"}

@pytest.fixture(scope="module")
def test_log_dir():
    """创建测试日志目录和文件"""
    # 指定测试用的日志目录
    test_dir = Path("logs")
    
    # 创建测试目录
    if not test_dir.exists():
        test_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建测试日志文件
    latest_log = test_dir / "latest.log"
    error_log = test_dir / "errors.log"
    
    # 写入测试日志内容
    with open(latest_log, "w", encoding="utf-8") as f:
        f.write("\n".join([
            "2023-05-23 10:00:12 [INFO] 服务启动成功，监听端口: 8080",
            "2023-05-23 10:05:23 [INFO] 用户登录: test_user (IP: 192.168.1.100)",
            "2023-05-23 10:10:45 [INFO] 处理请求: /api/settings/model",
            "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败: 401 Unauthorized"
        ]))
    
    with open(error_log, "w", encoding="utf-8") as f:
        f.write("\n".join([
            "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败: 401 Unauthorized",
            "2023-05-23 10:20:45 [ERROR] 连接超时: https://example.com/api/v1",
            "2023-05-23 11:05:10 [ERROR] JSON解析错误: Unexpected token"
        ]))
    
    yield test_dir
    
    # 测试后不删除日志文件，以便检查

def test_get_latest_logs():
    """测试获取最新日志API"""
    response = client.post(
        "/api/logs/latest",
        headers=HEADERS,
        json={}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    assert "logs" in data["body"]
    assert isinstance(data["body"]["logs"], list)
    assert len(data["body"]["logs"]) > 0

def test_get_error_logs():
    """测试获取错误日志API"""
    response = client.post(
        "/api/logs/errors",
        headers=HEADERS,
        json={}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    assert "logs" in data["body"]
    assert isinstance(data["body"]["logs"], list)
    assert len(data["body"]["logs"]) > 0
    
    # 验证返回的是错误日志（包含error, exception等关键词）
    for log in data["body"]["logs"]:
        assert any(keyword in log.lower() for keyword in ["error", "exception", "fail"])

def test_get_logs_with_line_count():
    """测试指定行数获取日志"""
    line_count = 2
    response = client.post(
        "/api/logs/latest",
        headers=HEADERS,
        json={"line_count": line_count}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    assert len(data["body"]["logs"]) <= line_count

def test_get_logs_without_auth():
    """测试无认证获取日志（应当失败）"""
    response = client.post(
        "/api/logs/latest",
        headers={"Content-Type": "application/json"},  # 不包含auth头
        json={}
    )
    assert response.status_code == 401  # 或其他未授权状态码，取决于应用设置 