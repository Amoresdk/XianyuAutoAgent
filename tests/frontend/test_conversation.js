// conversation.js 的测试用例
// 使用 jest 框架和 jsdom 进行前端测试

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// 模拟API响应
const mockApiResponses = {
  "/api/conversations/statistics": {
    error: 0,
    body: {
      todayAmount: 3250,
      todayVisitors: 128,
      todayOrders: 42,
      conversionRate: 32.8,
      totalAmount: 125600,
      totalConversations: 1542
    },
    message: ""
  },
  "/api/conversations/list": {
    error: 0,
    body: {
      conversations: [
        {
          id: "conv_001",
          user_name: "张先生",
          last_message: "能再便宜点不，1200行不？",
          unread_count: 1,
          timestamp: "2023-05-21T10:18:00Z"
        },
        {
          id: "conv_002",
          user_name: "李女士",
          last_message: "你好，这个笔记本有发票吗？",
          unread_count: 0,
          timestamp: "2023-05-20T15:40:00Z"
        }
      ],
      total: 2,
      hasMore: false
    },
    message: ""
  },
  "/api/conversations/info": {
    error: 0,
    body: {
      id: "conv_001",
      status: "active",
      created_at: "2023-05-21T09:15:00Z",
      product: {
        id: "prod_001",
        title: "二手相机 佳能5D Mark IV 成色95新",
        price: 1299.00,
        image: "https://via.placeholder.com/50",
        description: "佳能5D4单反相机，2020年购入，非常爱惜，无磕碰无进水，快门数3000次左右，送存储卡、相机包和原装电池..."
      }
    },
    message: ""
  },
  "/api/conversations/messages": {
    error: 0,
    body: {
      messages: [
        {
          id: "msg_001",
          content: "这个相机能便宜点吗？",
          is_self: false,
          timestamp: "2023-05-21T10:15:00Z"
        },
        {
          id: "msg_002",
          content: "您好！感谢您对我这台佳能5D Mark IV的关注。这台相机的成色非常新，快门次数很少，而且我已经对价格进行了合理定位，相比市场价已经很优惠了。不过我理解您想要更好的价格，您能接受¥1250吗？",
          is_self: true,
          timestamp: "2023-05-21T10:16:00Z"
        },
        {
          id: "msg_003",
          content: "能再便宜点不，1200行不？",
          is_self: false,
          timestamp: "2023-05-21T10:18:00Z"
        }
      ],
      hasMore: false,
      total: 3
    },
    message: ""
  },
  "/api/conversations/send": {
    error: 0,
    body: {
      id: "msg_004",
      content: "好的，考虑到您的诚意，1200可以成交。您什么时候方便交易呢？",
      is_self: true,
      timestamp: "2023-05-21T10:25:00Z"
    },
    message: "消息已发送"
  }
};

// 设置全局变量
global.localStorage = {
  getItem: jest.fn(),
  setItem: jest.fn()
};

describe('对话管理页面测试', () => {
  let dom, window, document;
  
  beforeEach(() => {
    // 加载HTML
    const html = fs.readFileSync(path.resolve(__dirname, '../../frontend/pages/conversation.html'), 'utf8');
    dom = new JSDOM(html, {
      url: 'http://localhost/',
      runScripts: 'dangerously',
      resources: 'usable'
    });
    
    window = dom.window;
    document = window.document;
    
    // 模拟fetch
    global.fetch = jest.fn().mockImplementation((url, options) => {
      // 获取API路径
      const apiPath = new URL(url, 'http://localhost/').pathname;
      
      // 根据请求路径与方法返回不同的mock数据
      let mockResponse;
      
      if (apiPath === '/api/conversations/send') {
        mockResponse = mockApiResponses[apiPath];
      } else if (apiPath === '/api/conversations/info' || apiPath === '/api/conversations/messages') {
        const body = JSON.parse(options.body);
        if (body && body.id === 'conv_001') {
          mockResponse = mockApiResponses[apiPath];
        } else {
          mockResponse = {
            error: 404,
            body: {},
            message: '对话不存在'
          };
        }
      } else {
        mockResponse = mockApiResponses[apiPath] || {
          error: 404,
          body: {},
          message: '未找到匹配的mock'
        };
      }
      
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      });
    });
    
    // 模拟console
    global.console = {
      log: jest.fn(),
      error: jest.fn()
    };
    
    // 注入脚本
    const scriptElement = document.createElement('script');
    scriptElement.textContent = fs.readFileSync(path.resolve(__dirname, '../../frontend/static/js/conversation.js'), 'utf8');
    document.body.appendChild(scriptElement);
    
    // 挂载全局函数
    window.selectConversation = function(id) {
      // 调用页面中的selectConversation函数
      eval(`selectConversation('${id}')`);
    };
  });
  
  afterEach(() => {
    jest.clearAllMocks();
  });
  
  test('页面加载时应该调用 loadStatistics 和 loadConversations 方法', async () => {
    // 触发DOMContentLoaded事件
    const event = new window.Event('DOMContentLoaded');
    window.document.dispatchEvent(event);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 验证fetch调用
    expect(global.fetch).toHaveBeenCalledWith('/api/conversations/statistics', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'auth': ''
      },
      body: JSON.stringify({})
    });
    
    expect(global.fetch).toHaveBeenCalledWith('/api/conversations/list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'auth': ''
      },
      body: JSON.stringify({})
    });
  });
  
  test('统计数据应该正确显示在页面上', async () => {
    // 触发DOMContentLoaded事件
    const event = new window.Event('DOMContentLoaded');
    window.document.dispatchEvent(event);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 验证统计数据是否正确显示
    expect(document.querySelector('.stats-card:nth-child(1) .stats-value').textContent).toBe('¥3250');
    expect(document.querySelector('.stats-card:nth-child(2) .stats-value').textContent).toBe('128');
    expect(document.querySelector('.stats-card:nth-child(3) .stats-value').textContent).toBe('42');
    expect(document.querySelector('.stats-card:nth-child(4) .stats-value').textContent).toBe('32.8%');
  });
  
  test('对话列表应该正确渲染', async () => {
    // 触发DOMContentLoaded事件
    const event = new window.Event('DOMContentLoaded');
    window.document.dispatchEvent(event);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 验证对话列表是否正确渲染
    const chatItems = document.querySelectorAll('.chat-item');
    expect(chatItems.length).toBe(2);
    
    // 验证第一个对话项
    expect(chatItems[0].getAttribute('data-id')).toBe('conv_001');
    expect(chatItems[0].querySelector('.chat-name').textContent.trim()).toBe('张先生');
    expect(chatItems[0].querySelector('.chat-preview').textContent.trim()).toBe('能再便宜点不，1200行不？');
    expect(chatItems[0].querySelector('.unread-badge')).not.toBeNull();
    
    // 验证第二个对话项
    expect(chatItems[1].getAttribute('data-id')).toBe('conv_002');
    expect(chatItems[1].querySelector('.chat-name').textContent.trim()).toBe('李女士');
    expect(chatItems[1].querySelector('.chat-preview').textContent.trim()).toBe('你好，这个笔记本有发票吗？');
    expect(chatItems[1].querySelector('.unread-badge')).toBeNull();
  });
  
  test('选择对话时应该加载对话信息和消息列表', async () => {
    // 触发DOMContentLoaded事件
    const event = new window.Event('DOMContentLoaded');
    window.document.dispatchEvent(event);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 选择第一个对话
    const firstConversation = document.querySelector('.chat-item[data-id="conv_001"]');
    const clickEvent = new window.Event('click');
    firstConversation.dispatchEvent(clickEvent);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 验证fetch调用
    expect(global.fetch).toHaveBeenCalledWith('/api/conversations/info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'auth': ''
      },
      body: JSON.stringify({ id: 'conv_001' })
    });
    
    expect(global.fetch).toHaveBeenCalledWith('/api/conversations/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'auth': ''
      },
      body: JSON.stringify({ id: 'conv_001' })
    });
    
    // 验证对话信息是否正确显示
    expect(document.querySelector('.product-name').textContent).toContain('张先生');
    expect(document.querySelector('.product-price').textContent).toBe('¥1299');
    
    // 验证消息列表是否正确渲染
    const messages = document.querySelectorAll('.message');
    expect(messages.length).toBe(3);
    
    // 验证第一条消息（买家）
    expect(messages[0].classList.contains('message-other')).toBeTruthy();
    expect(messages[0].querySelector('.message-content').textContent).toBe('这个相机能便宜点吗？');
    
    // 验证第二条消息（卖家/AI）
    expect(messages[1].classList.contains('message-self')).toBeTruthy();
    expect(messages[1].querySelector('.message-content').textContent).toContain('您好！感谢您对我这台佳能5D Mark IV的关注');
    
    // 验证第三条消息（买家）
    expect(messages[2].classList.contains('message-other')).toBeTruthy();
    expect(messages[2].querySelector('.message-content').textContent).toBe('能再便宜点不，1200行不？');
  });
  
  test('发送消息按钮应该正常工作', async () => {
    // 触发DOMContentLoaded事件
    const event = new window.Event('DOMContentLoaded');
    window.document.dispatchEvent(event);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 选择第一个对话
    const firstConversation = document.querySelector('.chat-item[data-id="conv_001"]');
    const clickEvent = new window.Event('click');
    firstConversation.dispatchEvent(clickEvent);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 在输入框中输入消息
    const inputField = document.querySelector('.chat-input input');
    inputField.value = '好的，可以成交';
    
    // 点击发送按钮
    const sendButton = document.querySelector('.chat-input button');
    sendButton.dispatchEvent(new window.Event('click'));
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 验证fetch调用
    expect(global.fetch).toHaveBeenCalledWith('/api/conversations/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'auth': ''
      },
      body: JSON.stringify({
        id: 'conv_001',
        content: '好的，可以成交'
      })
    });
    
    // 验证输入框是否被清空
    expect(inputField.value).toBe('');
  });
  
  test('刷新按钮应该重新加载对话列表', async () => {
    // 触发DOMContentLoaded事件
    const event = new window.Event('DOMContentLoaded');
    window.document.dispatchEvent(event);
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 清除之前的mock调用记录
    global.fetch.mockClear();
    
    // 点击刷新按钮
    const refreshButton = document.getElementById('refresh-button');
    refreshButton.dispatchEvent(new window.Event('click'));
    
    // 等待异步操作完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 验证fetch调用
    expect(global.fetch).toHaveBeenCalledWith('/api/conversations/list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'auth': ''
      },
      body: JSON.stringify({})
    });
  });
}); 