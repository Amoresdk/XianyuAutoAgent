# XianyuAutoAgent API文档

## 模型设置API

### 1. 获取模型设置

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

### 2. 保存模型设置

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

### 3. 更新单个设置项

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

### 4. 重置模型设置

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

### 1. 获取对话统计数据

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

### 2. 获取对话列表

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

### 3. 获取对话信息

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

### 4. 获取对话消息列表

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

### 5. 发送消息

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