import os
import json
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
import uvicorn
from pathlib import Path

app = FastAPI()

# 启用CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/pages", StaticFiles(directory="frontend/pages"), name="pages")

# 加载模拟数据
def load_mock_data(file_name):
    try:
        with open(f"frontend/static/mocks/{file_name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading mock data {file_name}: {e}")
        return {}

model_settings_mock = load_mock_data("model_settings")
conversation_mock = load_mock_data("conversation")

# 简单的认证中间件
async def verify_token(request: Request):
    auth_token = request.headers.get("auth") or request.headers.get("test-token")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user_id": "mock_user"}

# 首页重定向到model_settings.html
@app.get("/")
async def root():
    # 返回前端首页
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# 模型设置API
@app.post("/api/settings/model")
async def model_settings(request: Request, user: dict = Depends(verify_token)):
    try:
        body = await request.json()
    except:
        body = {}
    
    # 如果包含模型参数，则是保存请求
    if body and any(key in body for key in ["model", "apiKey", "apiEndpoint", "modelName", "cookies"]):
        return JSONResponse({
            "error": 0,
            "body": body,
            "message": "设置已成功保存"
        })
    
    # 否则是获取请求，返回模拟数据
    mock_file = Path("frontend/static/mocks/model_settings.json")
    if mock_file.exists():
        with open(mock_file, "r", encoding="utf-8") as f:
            return JSONResponse(json.load(f))
    
    # 如果没有模拟数据，返回默认值
    return JSONResponse({
        "error": 0,
        "body": {
            "model": "qwen",
            "apiKey": "sk-mockkey123456789",
            "apiEndpoint": "https://dashscope.aliyuncs.com/api/v1",
            "modelName": "qwen-max",
            "cookies": "mock_cookie=value; mock_session=123"
        },
        "message": ""
    })

@app.post("/api/settings/model/update")
async def update_model_setting(request: Request, user: dict = Depends(verify_token)):
    body = await request.json()
    if "key" not in body or "value" not in body:
        return JSONResponse({
            "error": 400,
            "body": {},
            "message": "缺少必要参数"
        })
    
    return JSONResponse({
        "error": 0,
        "body": {},
        "message": "设置项已成功保存"
    })

@app.post("/api/settings/model/reset")
async def reset_model_settings(request: Request, user: dict = Depends(verify_token)):
    return JSONResponse({
        "error": 0,
        "body": {
            "model": "qwen",
            "apiKey": "",
            "apiEndpoint": "https://dashscope.aliyuncs.com/api/v1",
            "modelName": "qwen-max",
            "cookies": ""
        },
        "message": "设置已重置为默认值"
    })

# 对话管理API
@app.post("/api/conversations/statistics")
async def conversation_statistics(request: Request):
    try:
        return conversation_mock["statistics"]
    except Exception as e:
        print(f"Error in conversation_statistics: {e}")
        return conversation_mock["error_response"]

@app.post("/api/conversations/list")
async def conversation_list(request: Request):
    try:
        return conversation_mock["conversation_list"]
    except Exception as e:
        print(f"Error in conversation_list: {e}")
        return conversation_mock["error_response"]

@app.post("/api/conversations/info")
async def conversation_info(request: Request):
    try:
        body = await request.json()
        if body.get("id") == "conv_001":
            return conversation_mock["conversation_info"]
        else:
            response = {"error": 404, "body": {}, "message": "对话不存在"}
            return response
    except Exception as e:
        print(f"Error in conversation_info: {e}")
        return conversation_mock["error_response"]

@app.post("/api/conversations/messages")
async def conversation_messages(request: Request):
    try:
        body = await request.json()
        if body.get("id") == "conv_001":
            return conversation_mock["conversation_messages"]
        else:
            response = {"error": 404, "body": {}, "message": "对话不存在"}
            return response
    except Exception as e:
        print(f"Error in conversation_messages: {e}")
        return conversation_mock["error_response"]

@app.post("/api/conversations/send")
async def send_message(request: Request):
    try:
        body = await request.json()
        if body.get("id") and body.get("content"):
            return conversation_mock["send_message"]
        else:
            response = {"error": 400, "body": {}, "message": "参数错误"}
            return response
    except Exception as e:
        print(f"Error in send_message: {e}")
        return conversation_mock["error_response"]

# API路由 - 获取所有敏感词
@app.post("/api/filter/words")
async def get_filter_words(request: Request, user: dict = Depends(verify_token)):
    mock_file = Path("frontend/static/mocks/filter_settings.json")
    if mock_file.exists():
        with open(mock_file, "r", encoding="utf-8") as f:
            return JSONResponse(json.load(f))
    
    return JSONResponse({
        "error": 0,
        "body": {
            "words": ["敏感词1", "违禁词", "色情", "赌博"],
            "total": 4
        },
        "message": ""
    })

# API路由 - 添加敏感词
@app.post("/api/filter/add")
async def add_filter_word(request: Request, user: dict = Depends(verify_token)):
    body = await request.json()
    if "word" not in body or not body["word"]:
        return JSONResponse({
            "error": 400,
            "body": {},
            "message": "敏感词不能为空"
        })
    
    return JSONResponse({
        "error": 0,
        "body": {"success": True},
        "message": "敏感词添加成功"
    })

# API路由 - 删除敏感词
@app.post("/api/filter/delete")
async def delete_filter_word(request: Request, user: dict = Depends(verify_token)):
    body = await request.json()
    if "word" not in body or not body["word"]:
        return JSONResponse({
            "error": 400,
            "body": {},
            "message": "敏感词不能为空"
        })
    
    return JSONResponse({
        "error": 0,
        "body": {"success": True},
        "message": "敏感词删除成功"
    })

# API路由 - 清空敏感词
@app.post("/api/filter/clear")
async def clear_filter_words(request: Request, user: dict = Depends(verify_token)):
    return JSONResponse({
        "error": 0,
        "body": {"success": True},
        "message": "敏感词列表已清空"
    })

# API路由 - 获取最新日志
@app.post("/api/logs/latest")
async def get_latest_logs(request: Request, user: dict = Depends(verify_token)):
    mock_file = Path("frontend/static/mocks/logs.json")
    if mock_file.exists():
        with open(mock_file, "r", encoding="utf-8") as f:
            return JSONResponse(json.load(f))
    
    return JSONResponse({
        "error": 0,
        "body": {
            "logs": [
                "2023-05-23 10:00:12 [INFO] 服务启动成功，监听端口: 8080",
                "2023-05-23 10:05:23 [INFO] 用户登录: admin_user (IP: 192.168.1.100)",
                "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败，错误代码: 401"
            ]
        },
        "message": ""
    })

# API路由 - 获取错误日志
@app.post("/api/logs/errors")
async def get_error_logs(request: Request, user: dict = Depends(verify_token)):
    mock_file = Path("frontend/static/mocks/error_logs.json")
    if mock_file.exists():
        with open(mock_file, "r", encoding="utf-8") as f:
            return JSONResponse(json.load(f))
    
    return JSONResponse({
        "error": 0,
        "body": {
            "logs": [
                "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败，错误代码: 401",
                "2023-05-23 10:20:45 [ERROR] 连接超时: https://api.example.com/v1/messages",
                "2023-05-23 11:05:10 [ERROR] 无法解析JSON响应: SyntaxError: Unexpected token"
            ]
        },
        "message": ""
    })

if __name__ == "__main__":
    uvicorn.run("mock_server:app", host="127.0.0.1", port=8000, reload=True) 