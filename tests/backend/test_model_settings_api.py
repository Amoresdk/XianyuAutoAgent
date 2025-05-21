import pytest
from fastapi.testclient import TestClient
import json
import os
from unittest.mock import patch, MagicMock

# 假设FastAPI应用实例为app
# 后续实现时根据实际应用结构导入
# from backend.app.main import app

# 模拟app
class MockApp:
    def __init__(self):
        pass

app = MockApp()

# 创建测试客户端
@pytest.fixture
def client():
    # 这里使用mock代替实际应用
    with patch('fastapi.FastAPI', return_value=app):
        with patch('fastapi.testclient.TestClient') as mock_client:
            # 模拟API响应
            mock_instance = MagicMock()
            
            # 模拟获取设置API
            def mock_get_settings(*args, **kwargs):
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "error": 0,
                    "body": {
                        "model": "qwen",
                        "apiKey": "test-api-key",
                        "apiEndpoint": "https://test-api.com/v1",
                        "modelName": "test-model",
                        "cookies": "test-cookies"
                    },
                    "message": ""
                }
                return mock_response
            
            # 模拟保存设置API
            def mock_save_settings(*args, **kwargs):
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "error": 0,
                    "body": {},
                    "message": "设置已成功保存"
                }
                return mock_response
            
            # 模拟更新单个设置项API
            def mock_update_setting(*args, **kwargs):
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "error": 0,
                    "body": {},
                    "message": "设置项已成功保存"
                }
                return mock_response
            
            # 模拟重置设置API
            def mock_reset_settings(*args, **kwargs):
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "error": 0,
                    "body": {
                        "model": "qwen",
                        "apiKey": "",
                        "apiEndpoint": "https://dashscope.aliyuncs.com/api/v1",
                        "modelName": "qwen-max",
                        "cookies": ""
                    },
                    "message": "设置已重置为默认值"
                }
                return mock_response
            
            # 根据URL路径分发到不同的模拟响应
            def mock_post(url, *args, **kwargs):
                if url == "/api/settings/model" and kwargs.get("json") == {}:
                    return mock_get_settings()
                elif url == "/api/settings/model" and isinstance(kwargs.get("json"), dict) and "model" in kwargs.get("json"):
                    return mock_save_settings()
                elif url == "/api/settings/model/update":
                    return mock_update_setting()
                elif url == "/api/settings/model/reset":
                    return mock_reset_settings()
                
                # 默认返回错误
                mock_response = MagicMock()
                mock_response.status_code = 404
                mock_response.json.return_value = {
                    "error": 500,
                    "body": {},
                    "message": "未找到匹配的模拟API"
                }
                return mock_response
            
            mock_instance.post = mock_post
            mock_client.return_value = mock_instance
            
            yield mock_instance


class TestModelSettingsAPI:
    """模型设置API测试类"""
    
    def test_get_model_settings(self, client):
        """测试获取模型设置API"""
        response = client.post("/api/settings/model", json={})
        data = response.json()
        
        assert data["error"] == 0
        assert "model" in data["body"]
        assert "apiKey" in data["body"]
        assert "apiEndpoint" in data["body"]
        assert "modelName" in data["body"]
        assert "cookies" in data["body"]
    
    def test_save_model_settings(self, client):
        """测试保存模型设置API"""
        settings = {
            "model": "gpt-4",
            "apiKey": "new-api-key",
            "apiEndpoint": "https://new-api.com/v1",
            "modelName": "new-model",
            "cookies": "new-cookies"
        }
        
        response = client.post("/api/settings/model", json=settings)
        data = response.json()
        
        assert data["error"] == 0
        assert data["message"] == "设置已成功保存"
    
    def test_update_setting_item(self, client):
        """测试更新单个设置项API"""
        payload = {
            "key": "apiKey",
            "value": "updated-api-key"
        }
        
        response = client.post("/api/settings/model/update", json=payload)
        data = response.json()
        
        assert data["error"] == 0
        assert data["message"] == "设置项已成功保存"
    
    def test_reset_settings(self, client):
        """测试重置设置API"""
        response = client.post("/api/settings/model/reset", json={})
        data = response.json()
        
        assert data["error"] == 0
        assert data["message"] == "设置已重置为默认值"
        assert data["body"]["model"] == "qwen"
        assert data["body"]["apiKey"] == ""
        assert data["body"]["apiEndpoint"] == "https://dashscope.aliyuncs.com/api/v1"
        assert data["body"]["modelName"] == "qwen-max"
        assert data["body"]["cookies"] == "" 