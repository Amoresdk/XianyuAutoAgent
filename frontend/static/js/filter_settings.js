// filter_settings.js - 敏感词过滤设置页面的交互逻辑
let filterWords = []; // 存储敏感词列表

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化加载敏感词列表
    loadFilterWords();
    
    // 绑定添加敏感词表单提交事件
    document.getElementById('addWordForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addFilterWord();
    });
});

// 从服务器加载敏感词列表
function loadFilterWords() {
    // 显示加载中状态
    showLoading(true);
    
    // 调用API获取敏感词列表
    fetch('/api/filter/words', {
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
            // 成功获取数据
            filterWords = data.body.words || [];
            updateWordsDisplay();
        } else {
            // 显示错误消息
            showToast('错误', data.message || '获取敏感词列表失败', 'error');
        }
    })
    .catch(error => {
        console.error('获取敏感词列表出错:', error);
        showToast('错误', '网络错误，请稍后重试', 'error');
    })
    .finally(() => {
        showLoading(false);
    });
}

// 更新敏感词列表显示
function updateWordsDisplay() {
    const container = document.getElementById('filterWordsContainer');
    const emptyState = document.getElementById('emptyState');
    const wordCounter = document.getElementById('wordCounter');
    
    // 更新计数器
    wordCounter.textContent = `${filterWords.length} 个词`;
    
    // 清空现有内容
    container.innerHTML = '';
    
    // 如果没有敏感词，显示空状态提示
    if (filterWords.length === 0) {
        container.appendChild(emptyState);
        return;
    }
    
    // 创建敏感词标签
    filterWords.forEach(word => {
        const wordTag = document.createElement('div');
        wordTag.className = 'filter-word-tag';
        
        // 词语内容
        const wordContent = document.createElement('span');
        wordContent.className = 'word-content';
        wordContent.textContent = word;
        wordTag.appendChild(wordContent);
        
        // 删除按钮
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-word-btn';
        deleteBtn.innerHTML = '<i class="fas fa-times"></i>';
        deleteBtn.setAttribute('data-word', word);
        deleteBtn.onclick = function() {
            confirmDeleteWord(word);
        };
        wordTag.appendChild(deleteBtn);
        
        container.appendChild(wordTag);
    });
}

// 添加敏感词
function addFilterWord() {
    const input = document.getElementById('newWord');
    const word = input.value.trim();
    
    // 验证输入
    if (!word) {
        showToast('提示', '请输入敏感词', 'warning');
        return;
    }
    
    // 检查是否已存在
    if (filterWords.includes(word)) {
        showToast('提示', '该敏感词已存在', 'warning');
        input.value = '';
        return;
    }
    
    // 显示加载中状态
    showLoading(true);
    
    // 调用API添加敏感词
    fetch('/api/filter/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({ word })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            // 添加成功
            filterWords.push(word);
            updateWordsDisplay();
            input.value = '';
            showToast('成功', '敏感词已添加', 'success');
        } else {
            // 显示错误消息
            showToast('错误', data.message || '添加敏感词失败', 'error');
        }
    })
    .catch(error => {
        console.error('添加敏感词出错:', error);
        showToast('错误', '网络错误，请稍后重试', 'error');
    })
    .finally(() => {
        showLoading(false);
    });
}

// 确认删除敏感词
function confirmDeleteWord(word) {
    // 设置确认模态框内容
    document.getElementById('confirmModalLabel').textContent = '确认删除';
    document.getElementById('confirmModalBody').textContent = `确定要删除敏感词 "${word}" 吗？`;
    
    // 设置确认按钮点击事件
    const confirmBtn = document.getElementById('confirmActionBtn');
    confirmBtn.onclick = function() {
        deleteFilterWord(word);
        // 关闭模态框
        const modal = bootstrap.Modal.getInstance(document.getElementById('confirmModal'));
        modal.hide();
    };
    
    // 显示确认模态框
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
}

// 删除单个敏感词
function deleteFilterWord(word) {
    // 显示加载中状态
    showLoading(true);
    
    // 调用API删除敏感词
    fetch('/api/filter/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({ word })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            // 删除成功
            filterWords = filterWords.filter(w => w !== word);
            updateWordsDisplay();
            showToast('成功', '敏感词已删除', 'success');
        } else {
            // 显示错误消息
            showToast('错误', data.message || '删除敏感词失败', 'error');
        }
    })
    .catch(error => {
        console.error('删除敏感词出错:', error);
        showToast('错误', '网络错误，请稍后重试', 'error');
    })
    .finally(() => {
        showLoading(false);
    });
}

// 清空所有敏感词
function clearAllWords() {
    // 设置确认模态框内容
    document.getElementById('confirmModalLabel').textContent = '确认清空';
    document.getElementById('confirmModalBody').textContent = '确定要清空所有敏感词吗？此操作不可恢复。';
    
    // 设置确认按钮点击事件
    const confirmBtn = document.getElementById('confirmActionBtn');
    confirmBtn.onclick = function() {
        // 显示加载中状态
        showLoading(true);
        
        // 调用API清空敏感词列表
        fetch('/api/filter/clear', {
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
                // 清空成功
                filterWords = [];
                updateWordsDisplay();
                showToast('成功', '敏感词列表已清空', 'success');
            } else {
                // 显示错误消息
                showToast('错误', data.message || '清空敏感词列表失败', 'error');
            }
        })
        .catch(error => {
            console.error('清空敏感词列表出错:', error);
            showToast('错误', '网络错误，请稍后重试', 'error');
        })
        .finally(() => {
            showLoading(false);
        });
        
        // 关闭模态框
        const modal = bootstrap.Modal.getInstance(document.getElementById('confirmModal'));
        modal.hide();
    };
    
    // 显示确认模态框
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
}

// 辅助函数：显示加载中状态
function showLoading(isLoading) {
    // 这里可以实现加载中的UI显示
    // 例如显示/隐藏一个加载中的spinner
    // 暂时留空，根据实际UI设计实现
}

// 辅助函数：显示toast消息
function showToast(title, message, type) {
    // 这里可以实现toast消息的显示
    // 暂时使用alert，后续可以替换为更好的UI组件
    alert(`${title}: ${message}`);
} 