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
            
            # 模拟获取统计数据API
            def mock_get_statistics(*args, **kwargs):
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "error": 0,
                    "body": {
                        "todayAmount": 3250,
                        "todayVisitors": 128,
                        "todayOrders": 42,
                        "conversionRate": 32.8,
                        "totalAmount": 125600,
                        "totalConversations": 1542
                    },
                    "message": ""
                }
                return mock_response
            
            # 模拟获取对话列表API
            def mock_get_conversations(*args, **kwargs):
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "error": 0,
                    "body": {
                        "conversations": [
                            {
                                "id": "conv_001",
                                "user_name": "张先生",
                                "last_message": "能再便宜点不，1200行不？",
                                "unread_count": 1,
                                "timestamp": "2023-05-21T10:18:00Z"
                            },
                            {
                                "id": "conv_002",
                                "user_name": "李女士",
                                "last_message": "你好，这个笔记本有发票吗？",
                                "unread_count": 0,
                                "timestamp": "2023-05-20T15:40:00Z"
                            }
                        ],
                        "total": 2,
                        "hasMore": False
                    },
                    "message": ""
                }
                return mock_response
            
            # 模拟获取对话信息API
            def mock_get_conversation_info(*args, **kwargs):
                request_json = kwargs.get('json', {})
                conv_id = request_json.get('id')
                
                if conv_id == 'conv_001':
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = {
                        "error": 0,
                        "body": {
                            "id": "conv_001",
                            "status": "active",
                            "created_at": "2023-05-21T09:15:00Z",
                            "product": {
                                "id": "prod_001",
                                "title": "二手相机 佳能5D Mark IV 成色95新",
                                "price": 1299.00,
                                "image": "https://via.placeholder.com/50",
                                "description": "佳能5D4单反相机，2020年购入，非常爱惜，无磕碰无进水，快门数3000次左右，送存储卡、相机包和原装电池..."
                            }
                        },
                        "message": ""
                    }
                    return mock_response
                else:
                    mock_response = MagicMock()
                    mock_response.status_code = 404
                    mock_response.json.return_value = {
                        "error": 404,
                        "body": {},
                        "message": "对话不存在"
                    }
                    return mock_response
            
            # 模拟获取对话消息API
            def mock_get_conversation_messages(*args, **kwargs):
                request_json = kwargs.get('json', {})
                conv_id = request_json.get('id')
                
                if conv_id == 'conv_001':
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = {
                        "error": 0,
                        "body": {
                            "messages": [
                                {
                                    "id": "msg_001",
                                    "content": "这个相机能便宜点吗？",
                                    "is_self": False,
                                    "timestamp": "2023-05-21T10:15:00Z"
                                },
                                {
                                    "id": "msg_002",
                                    "content": "您好！感谢您对我这台佳能5D Mark IV的关注。这台相机的成色非常新，快门次数很少，而且我已经对价格进行了合理定位，相比市场价已经很优惠了。不过我理解您想要更好的价格，您能接受¥1250吗？",
                                    "is_self": True,
                                    "timestamp": "2023-05-21T10:16:00Z"
                                },
                                {
                                    "id": "msg_003",
                                    "content": "能再便宜点不，1200行不？",
                                    "is_self": False,
                                    "timestamp": "2023-05-21T10:18:00Z"
                                }
                            ],
                            "hasMore": False,
                            "total": 3
                        },
                        "message": ""
                    }
                    return mock_response
                else:
                    mock_response = MagicMock()
                    mock_response.status_code = 404
                    mock_response.json.return_value = {
                        "error": 404,
                        "body": {},
                        "message": "对话不存在"
                    }
                    return mock_response
            
            # 模拟发送消息API
            def mock_send_message(*args, **kwargs):
                request_json = kwargs.get('json', {})
                conv_id = request_json.get('id')
                content = request_json.get('content')
                
                if conv_id == 'conv_001' and content:
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = {
                        "error": 0,
                        "body": {
                            "id": "msg_004",
                            "content": content,
                            "is_self": True,
                            "timestamp": "2023-05-21T10:25:00Z"
                        },
                        "message": "消息已发送"
                    }
                    return mock_response
                else:
                    mock_response = MagicMock()
                    mock_response.status_code = 400
                    mock_response.json.return_value = {
                        "error": 400,
                        "body": {},
                        "message": "参数错误"
                    }
                    return mock_response
            
            # 根据URL路径分发到不同的模拟响应
            def mock_post(url, *args, **kwargs):
                if url == "/api/conversations/statistics":
                    return mock_get_statistics()
                elif url == "/api/conversations/list":
                    return mock_get_conversations()
                elif url == "/api/conversations/info":
                    return mock_get_conversation_info(*args, **kwargs)
                elif url == "/api/conversations/messages":
                    return mock_get_conversation_messages(*args, **kwargs)
                elif url == "/api/conversations/send":
                    return mock_send_message(*args, **kwargs)
                
                # 默认返回错误
                mock_response = MagicMock()
                mock_response.status_code = 404
                mock_response.json.return_value = {
                    "error": 404,
                    "body": {},
                    "message": "未找到匹配的API"
                }
                return mock_response
            
            mock_instance.post = mock_post
            mock_client.return_value = mock_instance
            
            yield mock_instance


class TestConversationAPI:
    """对话管理API测试类"""
    
    def test_get_statistics(self, client):
        """测试获取统计数据API"""
        response = client.post("/api/conversations/statistics", json={})
        data = response.json()
        
        assert data["error"] == 0
        assert "todayAmount" in data["body"]
        assert "todayVisitors" in data["body"]
        assert "todayOrders" in data["body"]
        assert "conversionRate" in data["body"]
        assert data["body"]["todayAmount"] == 3250
        assert data["body"]["todayVisitors"] == 128
        assert data["body"]["todayOrders"] == 42
        assert data["body"]["conversionRate"] == 32.8
    
    def test_get_conversations(self, client):
        """测试获取对话列表API"""
        response = client.post("/api/conversations/list", json={})
        data = response.json()
        
        assert data["error"] == 0
        assert "conversations" in data["body"]
        assert len(data["body"]["conversations"]) == 2
        assert data["body"]["conversations"][0]["id"] == "conv_001"
        assert data["body"]["conversations"][0]["user_name"] == "张先生"
        assert data["body"]["conversations"][1]["id"] == "conv_002"
        assert data["body"]["conversations"][1]["user_name"] == "李女士"
    
    def test_get_conversation_info(self, client):
        """测试获取对话信息API"""
        # 测试存在的对话
        response = client.post("/api/conversations/info", json={"id": "conv_001"})
        data = response.json()
        
        assert data["error"] == 0
        assert data["body"]["id"] == "conv_001"
        assert data["body"]["status"] == "active"
        assert "product" in data["body"]
        assert data["body"]["product"]["title"] == "二手相机 佳能5D Mark IV 成色95新"
        assert data["body"]["product"]["price"] == 1299.00
        
        # 测试不存在的对话
        response = client.post("/api/conversations/info", json={"id": "non_existent"})
        data = response.json()
        
        assert data["error"] == 404
        assert data["message"] == "对话不存在"
    
    def test_get_conversation_messages(self, client):
        """测试获取对话消息列表API"""
        # 测试存在的对话
        response = client.post("/api/conversations/messages", json={"id": "conv_001"})
        data = response.json()
        
        assert data["error"] == 0
        assert "messages" in data["body"]
        assert len(data["body"]["messages"]) == 3
        assert data["body"]["messages"][0]["id"] == "msg_001"
        assert data["body"]["messages"][0]["content"] == "这个相机能便宜点吗？"
        assert data["body"]["messages"][0]["is_self"] == False
        
        # 测试不存在的对话
        response = client.post("/api/conversations/messages", json={"id": "non_existent"})
        data = response.json()
        
        assert data["error"] == 404
        assert data["message"] == "对话不存在"
    
    def test_send_message(self, client):
        """测试发送消息API"""
        # 测试发送有效消息
        response = client.post("/api/conversations/send", json={
            "id": "conv_001",
            "content": "好的，考虑到您的诚意，1200可以成交。您什么时候方便交易呢？"
        })
        data = response.json()
        
        assert data["error"] == 0
        assert data["body"]["id"] == "msg_004"
        assert data["body"]["content"] == "好的，考虑到您的诚意，1200可以成交。您什么时候方便交易呢？"
        assert data["body"]["is_self"] == True
        
        # 测试发送无效消息（空内容）
        response = client.post("/api/conversations/send", json={
            "id": "conv_001",
            "content": ""
        })
        data = response.json()
        
        assert data["error"] == 400
        assert data["message"] == "参数错误"
        
        # 测试发送到不存在的对话
        response = client.post("/api/conversations/send", json={
            "id": "non_existent",
            "content": "这是一条测试消息"
        })
        data = response.json()
        
        assert data["error"] == 400
        assert data["message"] == "参数错误" 