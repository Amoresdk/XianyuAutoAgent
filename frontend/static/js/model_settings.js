// 模型配置信息
const modelConfigs = {
    'qwen': {
        name: '通义千问',
        endpoint: 'https://dashscope.aliyuncs.com/api/v1',
        modelName: 'qwen-max',
        description: '通义千问是阿里云自研大语言模型，具有较强的中文理解能力和对话能力。'
    },
    'gpt-4': {
        name: 'GPT-4',
        endpoint: 'https://api.openai.com/v1',
        modelName: 'gpt-4-turbo',
        description: 'OpenAI的GPT-4是目前最先进的大语言模型之一，具有强大的推理和创作能力。'
    },
    'gpt-3.5': {
        name: 'GPT-3.5',
        endpoint: 'https://api.openai.com/v1',
        modelName: 'gpt-3.5-turbo',
        description: 'GPT-3.5提供良好的性能与速度平衡，适合一般对话和客服场景。'
    },
    'wenxin': {
        name: '文心一言',
        endpoint: 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop',
        modelName: 'ernie-4.0',
        description: '百度文心一言是国内领先的大语言模型，拥有丰富的中文知识和对话能力。'
    },
    'custom': {
        name: '自定义模型',
        endpoint: '',
        modelName: '',
        description: '配置自定义模型接口和参数，适用于私有部署或其他第三方模型。'
    }
};

// 当前选择的模型
let currentModel = 'qwen';

// 页面加载时获取配置
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
});

// 选择模型
function selectModel(element) {
    // 移除所有模型卡片的选中状态
    document.querySelectorAll('.model-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // 添加当前模型卡片的选中状态
    element.classList.add('selected');
    
    // 保存当前选择的模型
    currentModel = element.dataset.model;
    
    // 根据选择的模型更新接口地址和模型名称
    updateInterfaceByModel(currentModel);
    
    // 保存设置
    saveSettings();
}

// 根据模型更新接口信息
function updateInterfaceByModel(model) {
    const endpointInput = document.getElementById('apiEndpoint');
    const modelNameInput = document.getElementById('modelName');
    
    switch(model) {
        case 'qwen':
            endpointInput.value = 'https://dashscope.aliyuncs.com/api/v1';
            modelNameInput.value = 'qwen-max';
            break;
        case 'gpt-4':
            endpointInput.value = 'https://api.openai.com/v1';
            modelNameInput.value = 'gpt-4';
            break;
        case 'gpt-3.5':
            endpointInput.value = 'https://api.openai.com/v1';
            modelNameInput.value = 'gpt-3.5-turbo';
            break;
        case 'wenxin':
            endpointInput.value = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1';
            modelNameInput.value = 'wenxin-4.0';
            break;
        case 'custom':
            // 自定义模型不更改当前值，让用户自行输入
            break;
    }
}

// 切换API密钥可见性
function toggleApiKeyVisibility() {
    const apiKeyInput = document.getElementById('apiKey');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (apiKeyInput.type === 'password') {
        apiKeyInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        apiKeyInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// 保存单个设置
function saveApiKey() {
    const apiKey = document.getElementById('apiKey').value;
    saveModelSetting('apiKey', apiKey);
}

function saveEndpoint() {
    const apiEndpoint = document.getElementById('apiEndpoint').value;
    saveModelSetting('apiEndpoint', apiEndpoint);
}

function saveModelName() {
    const modelName = document.getElementById('modelName').value;
    saveModelSetting('modelName', modelName);
}

function saveCookies() {
    const cookies = document.getElementById('cookies').value;
    saveModelSetting('cookies', cookies);
}

// 保存所有设置
function saveAllSettings() {
    saveSettings();
    showMessage('所有设置已保存', 'success');
}

// 保存设置到后端
function saveSettings() {
    const settings = {
        model: currentModel,
        apiKey: document.getElementById('apiKey').value,
        apiEndpoint: document.getElementById('apiEndpoint').value,
        modelName: document.getElementById('modelName').value,
        cookies: document.getElementById('cookies').value
    };
    
    fetch('/api/settings/model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            console.log('设置已保存');
        } else {
            console.error('保存设置失败:', data.message);
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
    });
}

// 单个设置保存
function saveModelSetting(key, value) {
    const setting = {
        key: key,
        value: value
    };
    
    fetch('/api/settings/model/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify(setting)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            console.log(`设置项 ${key} 已保存`);
        } else {
            console.error(`保存设置项 ${key} 失败:`, data.message);
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
    });
}

// 加载设置
function loadSettings() {
    fetch('/api/settings/model', {
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
            const settings = data.body;
            
            // 更新表单值
            if (settings.model) {
                currentModel = settings.model;
                document.querySelectorAll('.model-card').forEach(card => {
                    if (card.dataset.model === currentModel) {
                        card.classList.add('selected');
                    } else {
                        card.classList.remove('selected');
                    }
                });
            }
            
            if (settings.apiKey) {
                document.getElementById('apiKey').value = settings.apiKey;
            }
            
            if (settings.apiEndpoint) {
                document.getElementById('apiEndpoint').value = settings.apiEndpoint;
            }
            
            if (settings.modelName) {
                document.getElementById('modelName').value = settings.modelName;
            }
            
            if (settings.cookies) {
                document.getElementById('cookies').value = settings.cookies;
            }
        } else {
            console.error('加载设置失败:', data.message);
        }
    })
    .catch(error => {
        console.error('API请求错误:', error);
    });
}

// 重置为默认配置
function resetToDefaults() {
    if (confirm('确定要重置所有设置到默认值吗？')) {
        fetch('/api/settings/model/reset', {
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
                loadSettings(); // 重新加载默认设置
                showMessage('已重置为默认配置', 'success');
            } else {
                showMessage('重置失败: ' + data.message, 'error');
            }
        })
        .catch(error => {
            showMessage('API请求错误', 'error');
            console.error('API请求错误:', error);
        });
    }
}

// 显示消息
function showMessage(message, type = 'info') {
    // 创建消息元素
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type === 'error' ? 'danger' : type} message-toast`;
    messageDiv.innerHTML = message;
    document.body.appendChild(messageDiv);
    
    // 3秒后自动消失
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 500);
    }, 3000);
}