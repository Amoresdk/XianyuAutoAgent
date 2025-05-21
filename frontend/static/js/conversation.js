// 全局变量
let currentConversationId = null; // 当前选中的对话ID
let conversations = []; // 所有对话列表
let messages = []; // 当前对话的消息列表
let statisticsData = {}; // 统计数据

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    // 加载统计数据
    loadStatistics();
    
    // 加载对话列表
    loadConversations();
    
    // 设置发送消息按钮事件
    document.querySelector('.chat-input button').addEventListener('click', sendMessage);
    
    // 设置输入框回车事件
    document.querySelector('.chat-input input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // 设置刷新按钮事件
    document.getElementById('refresh-button').addEventListener('click', () => {
        loadConversations();
        if (currentConversationId) {
            loadMessages(currentConversationId);
        }
    });
});

// 加载统计数据
function loadStatistics() {
    fetch('/api/conversations/statistics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            statisticsData = data.body;
            updateStatisticsUI(statisticsData);
        } else {
            console.error('加载统计数据失败:', data.message);
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
    });
}

// 更新统计数据UI
function updateStatisticsUI(data) {
    // 更新统计卡片
    document.querySelector('.stats-card:nth-child(1) .stats-value').textContent = `¥${data.todayAmount || 0}`;
    document.querySelector('.stats-card:nth-child(2) .stats-value').textContent = data.todayVisitors || 0;
    document.querySelector('.stats-card:nth-child(3) .stats-value').textContent = data.todayOrders || 0;
    document.querySelector('.stats-card:nth-child(4) .stats-value').textContent = `${data.conversionRate || 0}%`;
}

// 加载对话列表
function loadConversations() {
    // 显示加载中
    document.querySelector('.chat-list').innerHTML = `
        <div class="text-center p-4 text-muted">
            <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-2">加载用户列表中...</p>
        </div>
    `;
    
    fetch('/api/conversations/list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            conversations = data.body.conversations || [];
            renderConversationList(conversations);
        } else {
            console.error('加载对话列表失败:', data.message);
            document.querySelector('.chat-list').innerHTML = `
                <div class="text-center p-4 text-muted">
                    <p>加载失败，请重试</p>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
        document.querySelector('.chat-list').innerHTML = `
            <div class="text-center p-4 text-muted">
                <p>加载失败，请重试</p>
            </div>
        `;
    });
}

// 渲染对话列表
function renderConversationList(conversations) {
    const chatList = document.querySelector('.chat-list');
    
    if (conversations.length === 0) {
        chatList.innerHTML = `
            <div class="text-center p-4 text-muted">
                <p>暂无对话</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    conversations.forEach(conv => {
        const isActive = conv.id === currentConversationId;
        const unreadBadge = conv.unread_count > 0 ? `<span class="unread-badge">${conv.unread_count}</span>` : '';
        
        html += `
            <div class="chat-item ${isActive ? 'active' : ''}" data-id="${conv.id}" onclick="selectConversation('${conv.id}')">
                <div class="chat-avatar">
                    <span>${conv.user_name.substring(0, 1)}</span>
                </div>
                <div class="chat-info">
                    <div class="chat-name">
                        ${conv.user_name}
                        ${unreadBadge}
                    </div>
                    <div class="chat-preview">${conv.last_message || '暂无消息'}</div>
                </div>
            </div>
        `;
    });
    
    chatList.innerHTML = html;
}

// 选择对话
function selectConversation(conversationId) {
    // 如果已经选中，则不重复加载
    if (currentConversationId === conversationId) return;
    
    // 更新选中状态
    currentConversationId = conversationId;
    
    // 更新UI选中状态
    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`.chat-item[data-id="${conversationId}"]`).classList.add('active');
    
    // 加载对话信息
    loadConversationInfo(conversationId);
    
    // 加载消息列表
    loadMessages(conversationId);
}

// 加载对话信息（商品信息等）
function loadConversationInfo(conversationId) {
    fetch('/api/conversations/info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({ id: conversationId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            updateConversationInfoUI(data.body);
        } else {
            console.error('加载对话信息失败:', data.message);
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
    });
}

// 更新对话信息UI
function updateConversationInfoUI(info) {
    const productInfo = document.querySelector('.product-info');
    
    // 找到对应的对话
    const conversation = conversations.find(c => c.id === currentConversationId);
    
    if (info && info.product) {
        productInfo.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="${info.product.image || 'https://via.placeholder.com/50'}" class="product-image" alt="商品图片">
                <div>
                    <div class="product-name">
                        ${conversation ? conversation.user_name : '用户'} 
                        <small class="user-tag status-${info.status || 'pending'}">${getStatusText(info.status)}</small>
                    </div>
                    <div class="product-price">¥${info.product.price || '0.00'}</div>
                    <div class="product-meta">${info.product.title || '无商品信息'}</div>
                </div>
            </div>
        `;
    } else {
        productInfo.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="https://via.placeholder.com/50" class="product-image" alt="商品图片">
                <div>
                    <div class="product-name">
                        ${conversation ? conversation.user_name : '用户'}
                        <small class="user-tag status-pending">暂无状态</small>
                    </div>
                    <div class="product-price">¥0.00</div>
                    <div class="product-meta">无商品信息</div>
                </div>
            </div>
        `;
    }
}

// 获取状态文本
function getStatusText(status) {
    const statusMap = {
        'pending': '待处理',
        'active': '对话中',
        'completed': '已成交',
        'closed': '已关闭'
    };
    return statusMap[status] || '未知状态';
}

// 加载消息列表
function loadMessages(conversationId) {
    // 显示加载中
    document.querySelector('.chat-messages').innerHTML = `
        <div class="text-center p-4">
            <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">加载中...</span>
            </div>
            <p class="mt-2 text-muted">加载消息中...</p>
        </div>
    `;
    
    fetch('/api/conversations/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({ id: conversationId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            messages = data.body.messages || [];
            renderMessageList(messages);
        } else {
            console.error('加载消息失败:', data.message);
            document.querySelector('.chat-messages').innerHTML = `
                <div class="text-center p-4 text-muted">
                    <p>加载消息失败，请重试</p>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
        document.querySelector('.chat-messages').innerHTML = `
            <div class="text-center p-4 text-muted">
                <p>加载消息失败，请重试</p>
            </div>
        `;
    });
}

// 渲染消息列表
function renderMessageList(messages) {
    const chatMessages = document.querySelector('.chat-messages');
    
    if (messages.length === 0) {
        chatMessages.innerHTML = `
            <div class="text-center p-4 text-muted">
                <p>暂无消息记录</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    messages.forEach(msg => {
        const isMe = msg.is_self;
        const messageClass = isMe ? 'message-self' : 'message-other';
        
        html += `
            <div class="message ${messageClass}">
                <div class="message-content">${msg.content}</div>
                <div class="message-time">${formatTime(msg.timestamp)}</div>
            </div>
        `;
    });
    
    chatMessages.innerHTML = html;
    
    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 格式化时间
function formatTime(timestamp) {
    if (!timestamp) return '';
    
    const date = new Date(timestamp);
    const now = new Date();
    const isToday = date.getDate() === now.getDate() && 
                    date.getMonth() === now.getMonth() && 
                    date.getFullYear() === now.getFullYear();
    
    let formattedTime = '';
    
    if (isToday) {
        formattedTime = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    } else {
        formattedTime = date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }) + ' ' + 
                        date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    }
    
    return formattedTime;
}

// 发送消息
function sendMessage() {
    const inputElement = document.querySelector('.chat-input input');
    const content = inputElement.value.trim();
    
    if (!content) return;
    
    if (!currentConversationId) {
        alert('请先选择一个对话');
        return;
    }
    
    // 清空输入框
    inputElement.value = '';
    
    // 添加发送中的消息到UI
    const chatMessages = document.querySelector('.chat-messages');
    const newMessageElement = document.createElement('div');
    newMessageElement.className = 'message message-self';
    newMessageElement.innerHTML = `
        <div class="message-content">${content}</div>
        <div class="message-time">发送中...</div>
    `;
    chatMessages.appendChild(newMessageElement);
    
    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // 发送请求
    fetch('/api/conversations/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({
            id: currentConversationId,
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            // 重新加载消息列表
            loadMessages(currentConversationId);
        } else {
            console.error('发送消息失败:', data.message);
            newMessageElement.querySelector('.message-time').textContent = '发送失败';
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
        newMessageElement.querySelector('.message-time').textContent = '发送失败';
    });
} 