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
    test_file = test_dir / "filter_words.json"
    
    # 创建测试目录
    if not test_dir.exists():
        test_dir.mkdir(parents=True, exist_ok=True)
    
    # 准备测试数据
    test_data = ["测试敏感词1", "测试敏感词2", "测试敏感词3"]
    
    # 保存测试数据到文件
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    
    yield test_file
    
    # 清理测试文件
    if test_file.exists():
        os.remove(test_file)

def test_get_filter_words(test_config_file):
    """测试获取敏感词列表"""
    response = client.post("/api/filter/words", headers=HEADERS, json={})
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    assert "words" in data["body"]
    assert len(data["body"]["words"]) == 3
    assert "total" in data["body"]
    assert data["body"]["total"] == 3

def test_add_filter_word(test_config_file):
    """测试添加敏感词"""
    new_word = "新敏感词"
    response = client.post(
        "/api/filter/add",
        headers=HEADERS,
        json={"word": new_word}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    
    # 验证敏感词已添加
    response = client.post("/api/filter/words", headers=HEADERS, json={})
    data = response.json()
    assert new_word in data["body"]["words"]
    assert data["body"]["total"] == 4  # 原有3个词，新增1个

def test_add_existing_word(test_config_file):
    """测试添加已存在的敏感词"""
    existing_word = "测试敏感词1"  # 这个词在测试数据中已存在
    response = client.post(
        "/api/filter/add",
        headers=HEADERS,
        json={"word": existing_word}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 400
    assert "已存在" in data["message"]

def test_add_empty_word(test_config_file):
    """测试添加空敏感词"""
    response = client.post(
        "/api/filter/add",
        headers=HEADERS,
        json={"word": ""}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 400
    assert "不能为空" in data["message"]

def test_delete_filter_word(test_config_file):
    """测试删除敏感词"""
    word_to_delete = "测试敏感词2"  # 这个词在测试数据中存在
    response = client.post(
        "/api/filter/delete",
        headers=HEADERS,
        json={"word": word_to_delete}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    
    # 验证敏感词已删除
    response = client.post("/api/filter/words", headers=HEADERS, json={})
    data = response.json()
    assert word_to_delete not in data["body"]["words"]

def test_delete_nonexistent_word(test_config_file):
    """测试删除不存在的敏感词"""
    nonexistent_word = "不存在的敏感词"
    response = client.post(
        "/api/filter/delete",
        headers=HEADERS,
        json={"word": nonexistent_word}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 404
    assert "不存在" in data["message"]

def test_clear_all_words(test_config_file):
    """测试清空敏感词列表"""
    response = client.post(
        "/api/filter/clear",
        headers=HEADERS,
        json={}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == 0
    
    # 验证敏感词列表已清空
    response = client.post("/api/filter/words", headers=HEADERS, json={})
    data = response.json()
    assert len(data["body"]["words"]) == 0
    assert data["body"]["total"] == 0 