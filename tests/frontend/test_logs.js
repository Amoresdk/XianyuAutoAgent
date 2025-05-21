// test_logs.js - 日志页面前端测试

/**
 * 测试最新日志页面功能
 */
function testLogsPage() {
    console.log("=== 测试最新日志页面 ===");
    
    // 模拟fetch API返回的响应
    const mockResponse = {
        error: 0,
        body: {
            logs: [
                "2023-05-23 10:00:12 [INFO] 服务启动成功，监听端口: 8080",
                "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败，错误代码: 401",
                "2023-05-23 10:16:10 [INFO] 请求成功，获取到5条新消息"
            ]
        },
        message: ""
    };
    
    // 模拟DOM元素
    document.body.innerHTML = '<pre id="log">测试内容</pre>';
    
    // 模拟fetch函数
    global.fetch = jest.fn().mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(mockResponse)
        })
    );
    
    // 调用被测试函数
    fetchLogs();
    
    // 等待异步操作完成
    setTimeout(() => {
        // 验证fetch调用
        expect(fetch).toHaveBeenCalledWith('/api/logs/latest', expect.any(Object));
        
        // 验证DOM更新
        const logElement = document.getElementById('log');
        expect(logElement.innerHTML).toContain('服务启动成功');
        expect(logElement.innerHTML).toContain('<span class="error">');
        
        console.log("最新日志页面测试通过！");
    }, 100);
}

/**
 * 测试错误日志页面功能
 */
function testErrorLogsPage() {
    console.log("=== 测试错误日志页面 ===");
    
    // 模拟fetch API返回的响应
    const mockResponse = {
        error: 0,
        body: {
            logs: [
                "2023-05-23 10:15:32 [ERROR] 请求闲鱼API失败，错误代码: 401",
                "2023-05-23 10:20:45 [ERROR] 连接超时: https://api.example.com/v1/messages"
            ]
        },
        message: ""
    };
    
    // 模拟DOM元素
    document.body.innerHTML = '<pre id="log">测试内容</pre>';
    
    // 模拟fetch函数
    global.fetch = jest.fn().mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(mockResponse)
        })
    );
    
    // 调用被测试函数
    fetchErrorLogs();
    
    // 等待异步操作完成
    setTimeout(() => {
        // 验证fetch调用
        expect(fetch).toHaveBeenCalledWith('/api/logs/errors', expect.any(Object));
        
        // 验证DOM更新
        const logElement = document.getElementById('log');
        expect(logElement.innerHTML).toContain('请求闲鱼API失败');
        expect(logElement.innerHTML).toContain('连接超时');
        
        console.log("错误日志页面测试通过！");
    }, 100);
}

/**
 * 测试错误处理
 */
function testErrorHandling() {
    console.log("=== 测试错误处理 ===");
    
    // 模拟错误响应
    const mockErrorResponse = {
        error: 500,
        body: {},
        message: "服务器内部错误"
    };
    
    // 模拟DOM元素
    document.body.innerHTML = '<pre id="log">测试内容</pre>';
    
    // 模拟fetch函数返回错误
    global.fetch = jest.fn().mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(mockErrorResponse)
        })
    );
    
    // 调用被测试函数
    fetchLogs();
    
    // 等待异步操作完成
    setTimeout(() => {
        // 验证DOM更新为错误消息
        const logElement = document.getElementById('log');
        expect(logElement.innerText).toBe(mockErrorResponse.message || '日志加载失败');
        
        console.log("错误处理测试通过！");
    }, 100);
}

/**
 * 运行所有测试
 */
function runAllTests() {
    testLogsPage();
    testErrorLogsPage();
    testErrorHandling();
}

// 如果在Node.js环境中运行，导出测试函数；否则直接运行
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        testLogsPage,
        testErrorLogsPage,
        testErrorHandling,
        runAllTests
    };
} else {
    runAllTests();
} 