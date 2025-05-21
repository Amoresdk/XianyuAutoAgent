// model_settings.js 的测试用例
// 使用 jest 框架和 jsdom 进行前端测试

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// 模拟API响应
const mockApiResponses = {
    '/api/settings/model': {
        error: 0,
        body: {
            model: 'qwen',
            apiKey: 'test-api-key',
            apiEndpoint: 'https://test-api.com/v1',
            modelName: 'test-model',
            cookies: 'test-cookies'
        },
        message: ''
    },
    '/api/settings/model/update': {
        error: 0,
        body: {},
        message: '设置项已成功保存'
    },
    '/api/settings/model/reset': {
        error: 0,
        body: {
            model: 'qwen',
            apiKey: '',
            apiEndpoint: 'https://dashscope.aliyuncs.com/api/v1',
            modelName: 'qwen-max',
            cookies: ''
        },
        message: '设置已重置为默认值'
    }
};

// 设置全局变量
global.localStorage = {
    getItem: jest.fn(),
    setItem: jest.fn()
};

describe('模型设置页面测试', () => {
    let dom, window, document;
    
    beforeEach(() => {
        // 加载HTML
        const html = fs.readFileSync(path.resolve(__dirname, '../../frontend/pages/model_settings.html'), 'utf8');
        dom = new JSDOM(html, {
            url: 'http://localhost/',
            runScripts: 'dangerously',
            resources: 'usable'
        });
        
        window = dom.window;
        document = window.document;
        
        // 模拟fetch
        global.fetch = jest.fn().mockImplementation((url, options) => {
            const mockResponse = mockApiResponses[new URL(url, 'http://localhost/').pathname] || {
                error: 500,
                body: {},
                message: '未找到匹配的mock'
            };
            
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
        scriptElement.textContent = fs.readFileSync(path.resolve(__dirname, '../../frontend/static/js/model_settings.js'), 'utf8');
        document.body.appendChild(scriptElement);
    });
    
    afterEach(() => {
        jest.clearAllMocks();
    });
    
    test('页面加载时应该调用loadSettings方法获取设置', async () => {
        // 触发DOMContentLoaded事件
        const event = new window.Event('DOMContentLoaded');
        window.document.dispatchEvent(event);
        
        // 等待异步操作完成
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // 验证fetch调用
        expect(global.fetch).toHaveBeenCalledWith('/api/settings/model', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'auth': ''
            },
            body: JSON.stringify({})
        });
    });
    
    test('选择模型时应该更新接口信息', () => {
        // 获取模型卡片
        const gpt4Card = document.querySelector('[data-model="gpt-4"]');
        
        // 触发点击事件
        const clickEvent = new window.Event('click');
        gpt4Card.dispatchEvent(clickEvent);
        
        // 验证接口信息是否更新
        expect(document.getElementById('apiEndpoint').value).toBe('https://api.openai.com/v1');
        expect(document.getElementById('modelName').value).toBe('gpt-4');
    });
    
    test('保存单个设置项时应该调用API', async () => {
        // 设置API密钥
        const apiKeyInput = document.getElementById('apiKey');
        apiKeyInput.value = 'new-api-key';
        
        // 触发blur事件
        const blurEvent = new window.Event('blur');
        apiKeyInput.dispatchEvent(blurEvent);
        
        // 等待异步操作完成
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // 验证fetch调用
        expect(global.fetch).toHaveBeenCalledWith('/api/settings/model/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'auth': ''
            },
            body: JSON.stringify({
                key: 'apiKey',
                value: 'new-api-key'
            })
        });
    });
    
    test('保存所有设置时应该调用API', async () => {
        // 设置表单值
        document.getElementById('apiKey').value = 'all-api-key';
        document.getElementById('apiEndpoint').value = 'https://all-api.com/v1';
        document.getElementById('modelName').value = 'all-model';
        document.getElementById('cookies').value = 'all-cookies';
        
        // 触发保存按钮点击
        const saveButton = document.querySelector('.footer-buttons .btn-primary');
        const clickEvent = new window.Event('click');
        saveButton.dispatchEvent(clickEvent);
        
        // 等待异步操作完成
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // 验证fetch调用
        expect(global.fetch).toHaveBeenCalledWith('/api/settings/model', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'auth': ''
            },
            body: JSON.stringify({
                model: 'qwen', // 默认选择的是qwen
                apiKey: 'all-api-key',
                apiEndpoint: 'https://all-api.com/v1',
                modelName: 'all-model',
                cookies: 'all-cookies'
            })
        });
    });
    
    test('重置设置时应该调用API', async () => {
        // 模拟confirm返回true
        window.confirm = jest.fn().mockReturnValue(true);
        
        // 触发重置按钮点击
        const resetButton = document.querySelector('.footer-buttons .btn-outline-secondary');
        const clickEvent = new window.Event('click');
        resetButton.dispatchEvent(clickEvent);
        
        // 等待异步操作完成
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // 验证fetch调用
        expect(global.fetch).toHaveBeenCalledWith('/api/settings/model/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'auth': ''
            },
            body: JSON.stringify({})
        });
    });
}); 