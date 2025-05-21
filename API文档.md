# XianyuAutoAgent API文档

## 模型设置API

### 获取模型设置

- 接口名称：获取当前模型配置信息
- 接口地址：`/api/settings/model`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "model": "string",
    "apiKey": "string",
    "apiEndpoint": "string",
    "modelName": "string",
    "cookies": "string"
  },
  "message": ""
}
```
- 响应类型：json
- 字段说明：
  - model: 当前选择的模型类型，如 "qwen"、"gpt-4"、"gpt-3.5"、"wenxin"、"custom"
  - apiKey: API密钥
  - apiEndpoint: API接口地址
  - modelName: 模型名称
  - cookies: 闲鱼平台cookies

### 保存模型设置

- 接口名称：保存模型配置信息
- 接口地址：`/api/settings/model`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "model": "string",
  "apiKey": "string",
  "apiEndpoint": "string",
  "modelName": "string",
  "cookies": "string"
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {},
  "message": "设置已成功保存"
}
```
- 响应类型：json
- 字段说明：同获取模型设置接口

### 更新单个设置项

- 接口名称：更新单个模型配置项
- 接口地址：`/api/settings/model/update`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "key": "string",
  "value": "string"
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {},
  "message": "设置项已成功保存"
}
```
- 响应类型：json
- 字段说明：
  - key: 要更新的设置键名，可选值为 "model", "apiKey", "apiEndpoint", "modelName", "cookies"
  - value: 对应的设置值

### 重置模型设置

- 接口名称：重置模型配置为默认值
- 接口地址：`/api/settings/model/reset`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{}
```
- 响应参数：
```json
{
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
```
- 响应类型：json

## 对话管理API

### 获取对话统计数据

- 接口名称：获取对话统计数据
- 接口地址：`/api/conversations/statistics`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{}
```
- 响应参数：
```json
{
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
```
- 响应类型：json
- 字段说明：
  - todayAmount: 今日成交金额（元）
  - todayVisitors: 今日咨询人数
  - todayOrders: 今日下单人数
  - conversionRate: 转化率（百分比）
  - totalAmount: 累计成交金额（元，可选）
  - totalConversations: 累计对话数（可选）

### 获取对话列表

- 接口名称：获取对话列表
- 接口地址：`/api/conversations/list`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "conversations": [
      {
        "id": "string",
        "user_name": "string",
        "last_message": "string",
        "unread_count": 0,
        "timestamp": "string"
      }
    ],
    "total": 0,
    "hasMore": false
  },
  "message": ""
}
```
- 响应类型：json
- 字段说明：
  - conversations: 对话列表
    - id: 对话ID
    - user_name: 用户名称
    - last_message: 最后一条消息内容
    - unread_count: 未读消息数量
    - timestamp: 最后消息时间戳
  - total: 总对话数
  - hasMore: 是否有更多数据

### 获取对话信息

- 接口名称：获取单个对话的详细信息
- 接口地址：`/api/conversations/info`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "id": "string"
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "id": "string",
    "status": "string",
    "created_at": "string",
    "product": {
      "id": "string",
      "title": "string",
      "price": 0,
      "image": "string",
      "description": "string"
    }
  },
  "message": ""
}
```
- 响应类型：json
- 字段说明：
  - id: 对话ID
  - status: 对话状态，可选值 "pending"(待处理), "active"(对话中), "completed"(已成交), "closed"(已关闭)
  - created_at: 创建时间
  - product: 关联商品信息
    - id: 商品ID
    - title: 商品标题
    - price: 商品价格
    - image: 商品图片URL
    - description: 商品描述

### 获取对话消息列表

- 接口名称：获取对话消息列表
- 接口地址：`/api/conversations/messages`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "id": "string"
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "messages": [
      {
        "id": "string",
        "content": "string",
        "is_self": false,
        "timestamp": "string"
      }
    ],
    "hasMore": false,
    "total": 0
  },
  "message": ""
}
```
- 响应类型：json
- 字段说明：
  - messages: 消息列表
    - id: 消息ID
    - content: 消息内容
    - is_self: 是否是自己发送的消息（true表示商家/AI，false表示买家）
    - timestamp: 消息时间戳
  - hasMore: 是否有更多消息
  - total: 消息总数

### 发送消息

- 接口名称：向对话发送消息
- 接口地址：`/api/conversations/send`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "id": "string",
  "content": "string"
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "id": "string",
    "content": "string",
    "is_self": true,
    "timestamp": "string"
  },
  "message": "消息已发送"
}
```
- 响应类型：json
- 字段说明：
  - id: 新发送消息的ID
  - content: 消息内容
  - is_self: 是否是自己发送的消息（固定为true）
  - timestamp: 消息时间戳

## Agent设置相关API

### 获取所有Agent设置
- 接口名称：获取所有Agent的配置信息
- 接口地址：`/api/agents/settings`
- 方法：POST
- 需要登录：是
- 请求参数：
```
{}
```
- 响应参数：
```
{
  "error": 0,
  "body": {
    "agents": {
      "intent": {
        "enabled": true,
        "prompt": "string"
      },
      "sales": {
        "enabled": true,
        "prompt": "string"
      },
      "tech": {
        "enabled": true,
        "prompt": "string"
      },
      "price": {
        "enabled": true,
        "prompt": "string"
      }
    }
  },
  "message": ""
}
```
- 响应类型：json

### 切换Agent状态
- 接口名称：更新指定Agent的启用状态
- 接口地址：`/api/agents/toggle-status`
- 方法：POST
- 需要登录：是
- 请求参数：
```
{
  "agent_type": "string",  // 可选值: "intent", "sales", "tech", "price"
  "enabled": true  // 或 false
}
```
- 响应参数：
```
{
  "error": 0,
  "body": {
    "success": true
  },
  "message": ""
}
```
- 响应类型：json

### 更新Agent提示词
- 接口名称：更新指定Agent的提示词
- 接口地址：`/api/agents/update-prompt`
- 方法：POST
- 需要登录：是
- 请求参数：
```
{
  "agent_type": "string",  // 可选值: "intent", "sales", "tech", "price"
  "prompt": "string"  // 不能为空
}
```
- 响应参数：
```
{
  "error": 0,
  "body": {
    "success": true
  },
  "message": ""
}
```
- 响应类型：json

### 保存所有Agent设置
- 接口名称：一次性保存所有Agent的配置
- 接口地址：`/api/agents/save-all-settings`
- 方法：POST
- 需要登录：是
- 请求参数：
```
{
  "agents": {
    "intent": {
      "enabled": true,
      "prompt": "string"
    },
    "sales": {
      "enabled": true,
      "prompt": "string"
    },
    "tech": {
      "enabled": true,
      "prompt": "string"
    },
    "price": {
      "enabled": true,
      "prompt": "string"
    }
  }
}
```
- 响应参数：
```
{
  "error": 0,
  "body": {
    "success": true
  },
  "message": ""
}
```
- 响应类型：json

## 敏感词过滤API

### 获取敏感词列表
- 接口名称：获取所有已配置的敏感词
- 接口地址：`/api/filter/words`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "words": [
      "string",
      "string"
    ],
    "total": 0
  },
  "message": ""
}
```
- 响应类型：json
- 字段说明：
  - words: 敏感词列表
  - total: 敏感词总数

### 添加敏感词
- 接口名称：添加新的敏感词
- 接口地址：`/api/filter/add`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "word": "string"
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "success": true
  },
  "message": "敏感词添加成功"
}
```
- 响应类型：json
- 字段说明：
  - word: 要添加的敏感词

### 删除敏感词
- 接口名称：删除指定的敏感词
- 接口地址：`/api/filter/delete`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "word": "string"
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "success": true
  },
  "message": "敏感词删除成功"
}
```
- 响应类型：json
- 字段说明：
  - word: 要删除的敏感词

### 清空敏感词列表
- 接口名称：清空所有敏感词
- 接口地址：`/api/filter/clear`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "success": true
  },
  "message": "敏感词列表已清空"
}
```
- 响应类型：json

## 日志管理API

### 获取最新日志
- 接口名称：获取系统最新日志
- 接口地址：`/api/logs/latest`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "line_count": 100  // 可选，要获取的日志行数，默认100行
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "logs": [
      "2023-05-23 10:00:12 [INFO] 服务启动成功，监听端口: 8080",
      "2023-05-23 10:05:23 [INFO] 用户登录: admin_user (IP: 192.168.1.100)",
      "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败，错误代码: 401"
    ]
  },
  "message": ""
}
```
- 响应类型：json
- 字段说明：
  - logs: 日志行列表

### 获取错误日志
- 接口名称：获取系统错误日志
- 接口地址：`/api/logs/errors`
- 方法：POST
- 需要登录：是
- 请求参数：
```json
{
  "line_count": 100  // 可选，要获取的错误日志行数，默认100行
}
```
- 响应参数：
```json
{
  "error": 0,
  "body": {
    "logs": [
      "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败，错误代码: 401",
      "2023-05-23 10:20:45 [ERROR] 连接超时: https://api.example.com/v1/messages",
      "2023-05-23 11:05:10 [ERROR] 无法解析JSON响应: SyntaxError: Unexpected token"
    ]
  },
  "message": ""
}
```
- 响应类型：json
- 字段说明：
  - logs: 错误日志行列表
