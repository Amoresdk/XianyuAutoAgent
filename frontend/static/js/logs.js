// logs.js - 最新日志页面的交互逻辑

/**
 * 获取最新日志数据
 */
function fetchLogs() {
    // 显示加载状态
    document.getElementById('log').innerText = '加载中...';
    
    // 调用API获取最新日志
    fetch('/api/logs/latest', { 
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || '' 
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if(data.error === 0) {
            // 成功获取数据
            let lines = data.body.logs || [];
            
            // 处理日志行，对错误和异常信息添加样式
            document.getElementById('log').innerHTML = lines.map(line => {
                if(/error|exception/i.test(line)) {
                    return `<span class="error">${line}</span>`;
                }
                return line;
            }).join('\n');
            
            // 滚动到底部
            let logDiv = document.getElementById('log');
            logDiv.scrollTop = logDiv.scrollHeight;
        } else {
            // 显示错误消息
            document.getElementById('log').innerText = data.message || '日志加载失败';
        }
    })
    .catch(error => {
        console.error('获取最新日志失败:', error);
        document.getElementById('log').innerText = '网络错误，请稍后重试';
    });
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 立即加载一次日志
    fetchLogs();
    
    // 设置定时刷新（每2秒）
    setInterval(fetchLogs, 2000);
}); 