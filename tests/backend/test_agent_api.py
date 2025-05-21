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
HEADERS = {"test-token": TEST_TOKEN, "Content-Type": "application/json"}

@pytest.fixture(scope="module")
def test_config_file():
    """创建测试配置文件并在测试结束后删除"""
    # 指定测试用的配置文件路径
    test_dir = Path("backend/data")
    test_file = test_dir / "agent_settings.json"
    
    # 创建测试目录
    if not test_dir.exists():
        test_dir.mkdir(parents=True, exist_ok=True)
    
    # 准备测试数据
    test_data = {
        "intent": {"enabled": True, "prompt": "测试提示词1"},
        "sales": {"enabled": True, "prompt": "测试提示词2"},
        "tech": {"enabled": True, "prompt": "测试提示词3"},
        "price": {"enabled": False, "prompt": "测试提示词4"}
    }
    
    # 保存测试数据到文件
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    
    yield test_file
    
    # 清理测试文件
    if test_file.exists():
        os.remove(test_file)

def test_get_agent_settings(test_config_file):
    """测试获取所有Agent设置"""
    response = client.post("/api/agents/settings", headers=HEADERS, json={})
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    assert "agents" in data["body"]
    assert "intent" in data["body"]["agents"]
    assert "sales" in data["body"]["agents"]
    assert "tech" in data["body"]["agents"]
    assert "price" in data["body"]["agents"]

def test_toggle_agent_status(test_config_file):
    """测试切换Agent状态"""
    # 先确认当前状态
    response = client.post("/api/agents/settings", headers=HEADERS, json={})
    data = response.json()
    current_status = data["body"]["agents"]["tech"]["enabled"]
    
    # 切换状态
    new_status = not current_status
    response = client.post(
        "/api/agents/toggle-status", 
        headers=HEADERS, 
        json={"agent_type": "tech", "enabled": new_status}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    
    # 验证状态已更新
    response = client.post("/api/agents/settings", headers=HEADERS, json={})
    data = response.json()
    assert data["body"]["agents"]["tech"]["enabled"] == new_status

def test_update_agent_prompt(test_config_file):
    """测试更新Agent提示词"""
    new_prompt = "这是一个新的测试提示词"
    response = client.post(
        "/api/agents/update-prompt", 
        headers=HEADERS, 
        json={"agent_type": "sales", "prompt": new_prompt}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    
    # 验证提示词已更新
    response = client.post("/api/agents/settings", headers=HEADERS, json={})
    data = response.json()
    assert data["body"]["agents"]["sales"]["prompt"] == new_prompt

def test_save_all_agent_settings(test_config_file):
    """测试保存所有Agent设置"""
    # 准备新的设置数据
    new_settings = {
        "intent": {"enabled": False, "prompt": "新提示词1"},
        "sales": {"enabled": True, "prompt": "新提示词2"},
        "tech": {"enabled": False, "prompt": "新提示词3"},
        "price": {"enabled": True, "prompt": "新提示词4"}
    }
    
    response = client.post(
        "/api/agents/save-all-settings", 
        headers=HEADERS, 
        json={"agents": new_settings}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    
    # 验证所有设置已更新
    response = client.post("/api/agents/settings", headers=HEADERS, json={})
    data = response.json()
    agents = data["body"]["agents"]
    
    assert agents["intent"]["enabled"] == new_settings["intent"]["enabled"]
    assert agents["intent"]["prompt"] == new_settings["intent"]["prompt"]
    assert agents["sales"]["enabled"] == new_settings["sales"]["enabled"]
    assert agents["sales"]["prompt"] == new_settings["sales"]["prompt"]
    assert agents["tech"]["enabled"] == new_settings["tech"]["enabled"]
    assert agents["tech"]["prompt"] == new_settings["tech"]["prompt"]
    assert agents["price"]["enabled"] == new_settings["price"]["enabled"]
    assert agents["price"]["prompt"] == new_settings["price"]["prompt"]

def test_invalid_agent_type(test_config_file):
    """测试无效的Agent类型"""
    response = client.post(
        "/api/agents/toggle-status", 
        headers=HEADERS, 
        json={"agent_type": "invalid_type", "enabled": True}
    )
    assert response.status_code == 200  # 仍然返回200，但error不为0
    data = response.json()
    assert data["error"] == 400
    assert "无效的Agent类型" in data["message"]

def test_empty_prompt(test_config_file):
    """测试空提示词"""
    response = client.post(
        "/api/agents/update-prompt", 
        headers=HEADERS, 
        json={"agent_type": "tech", "prompt": ""}
    )
    assert response.status_code == 200  # 仍然返回200，但error不为0
    data = response.json()
    assert data["error"] == 400
    assert "提示词不能为空" in data["message"] 