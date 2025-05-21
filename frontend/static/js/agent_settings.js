// 存储提示词内容
const prompts = {
    intentPrompt: `您是闲鱼平台的智能客服系统中的意图分类专家。您的主要任务是分析用户消息的意图，并将请求路由到合适的专家Agent处理。
根据用户的消息，将用户意图分为以下几类：
1. 询价/讨价还价 - 由价格专家处理
2. 技术问题/产品使用方法 - 由技术专家处理
3. 一般咨询/售后/物流 - 由客服专家处理

请根据{conversation_history}中的对话历史，分析用户的真实意图，并返回相应的分类结果。`,
    salesPrompt: `您是闲鱼平台的专业客服代表。您需要帮助用户解决一般的咨询问题、售后问题和物流相关问题。
回复要求：
1. 语气友好、专业、有礼貌
2. 回答要简洁明了，直击问题核心
3. 适当使用表情符号增加亲和力
4. 为用户提供有价值的信息和解决方案
5. 必要时请用户提供更多细节以便更好地提供帮助

参考以下对话历史为用户{user_name}提供帮助：
{conversation_history}`,
    techPrompt: `您是闲鱼平台的技术支持专家。您的任务是解答用户关于产品使用、技术问题和功能咨询的问题。
回复要求：
1. 语气专业、清晰，使用技术术语要适度
2. 解释要详细但易于理解
3. 提供具体的步骤和解决方案
4. 如需引导用户操作，请给出明确的步骤指导
5. 必要时可以使用搜索工具获取最新的技术信息

请根据以下对话历史，为用户{user_name}解答关于{product_name}的技术问题：
{conversation_history}`,
    pricePrompt: `您是闲鱼平台的议价专家。您的任务是处理用户的砍价请求，在保证商家利益的同时，适度满足买家需求，达成交易。
价格策略指导：
1. 初始降价幅度不超过原价的10%
2. 最大降价幅度不超过原价的20%
3. 总共最多可降价3次，每次降价幅度递减
4. 强调商品价值和品质，而非仅关注价格
5. 适时提供促销信息或优惠方案

请根据以下对话历史，为{product_name}提供合理的价格方案：
{conversation_history}`
};

// 当前正在编辑的提示词类型
let currentPromptType = '';

// 显示提示词编辑模态框
function showPromptModal(agentName, promptType) {
    document.getElementById('promptModalLabel').innerText = `编辑${agentName}提示词`;
    document.getElementById('promptTextarea').value = prompts[promptType];
    currentPromptType = promptType;
    
    const promptModal = new bootstrap.Modal(document.getElementById('promptModal'));
    promptModal.show();
}

// 保存提示词
function savePrompt() {
    const newPrompt = document.getElementById('promptTextarea').value;
    prompts[currentPromptType] = newPrompt;
    
    // 关闭模态框
    const promptModal = bootstrap.Modal.getInstance(document.getElementById('promptModal'));
    promptModal.hide();
    
    // 显示成功消息
    alert('提示词已保存');
}

// 切换Agent状态
function toggleAgentStatus(cardId, isActive) {
    const statusElem = document.getElementById(cardId.replace('Card', 'Status'));
    if (isActive) {
        statusElem.innerText = '已启用';
        statusElem.className = 'agent-status status-active';
    } else {
        statusElem.innerText = '已禁用';
        statusElem.className = 'agent-status status-inactive';
    }
}

// 表单提交处理
document.getElementById('agentSettingsForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // 收集所有Agent的启用状态
    const agentStatus = {
        intent: document.getElementById('intentSwitch').checked,
        sales: document.getElementById('salesSwitch').checked,
        tech: document.getElementById('techSwitch').checked,
        price: document.getElementById('priceSwitch').checked
    };
    
    // 在这里可以添加将设置保存到服务器的代码
    console.log('Agent状态:', agentStatus);
    console.log('提示词配置:', prompts);
    
    // 使用API保存配置
    fetch('/api/agent_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            agents: agentStatus,
            prompts: prompts
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            alert('配置已保存');
        } else {
            alert('保存失败: ' + data.message);
        }
    })
    .catch(error => {
        console.error('保存配置出错:', error);
        // 即使API请求失败，也保存到本地，确保用户不会丢失设置
        localStorage.setItem('agentSettings', JSON.stringify({
            agents: agentStatus,
            prompts: prompts
        }));
        alert('无法连接到服务器，设置已保存到本地');
    });
});

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    // 尝试从服务器获取设置
    fetch('/api/agent_settings')
        .then(response => response.json())
        .then(data => {
            if (data.error === 0 && data.body) {
                // 更新Agent状态
                if (data.body.agents) {
                    const agents = data.body.agents;
                    document.getElementById('intentSwitch').checked = agents.intent;
                    document.getElementById('salesSwitch').checked = agents.sales;
                    document.getElementById('techSwitch').checked = agents.tech;
                    document.getElementById('priceSwitch').checked = agents.price;
                    
                    // 更新UI状态
                    toggleAgentStatus('intentCard', agents.intent);
                    toggleAgentStatus('salesCard', agents.sales);
                    toggleAgentStatus('techCard', agents.tech);
                    toggleAgentStatus('priceCard', agents.price);
                }
                
                // 更新提示词
                if (data.body.prompts) {
                    Object.assign(prompts, data.body.prompts);
                }
            } else {
                // 如果服务器没有数据，尝试从本地存储加载
                const savedSettings = localStorage.getItem('agentSettings');
                if (savedSettings) {
                    try {
                        const settings = JSON.parse(savedSettings);
                        if (settings.agents) {
                            const agents = settings.agents;
                            document.getElementById('intentSwitch').checked = agents.intent;
                            document.getElementById('salesSwitch').checked = agents.sales;
                            document.getElementById('techSwitch').checked = agents.tech;
                            document.getElementById('priceSwitch').checked = agents.price;
                            
                            // 更新UI状态
                            toggleAgentStatus('intentCard', agents.intent);
                            toggleAgentStatus('salesCard', agents.sales);
                            toggleAgentStatus('techCard', agents.tech);
                            toggleAgentStatus('priceCard', agents.price);
                        }
                        
                        if (settings.prompts) {
                            Object.assign(prompts, settings.prompts);
                        }
                    } catch (e) {
                        console.error('解析本地配置出错:', e);
                    }
                }
            }
        })
        .catch(error => {
            console.error('获取配置出错:', error);
            // 如果从服务器获取失败，尝试从本地存储加载
            const savedSettings = localStorage.getItem('agentSettings');
            if (savedSettings) {
                try {
                    const settings = JSON.parse(savedSettings);
                    if (settings.agents) {
                        const agents = settings.agents;
                        document.getElementById('intentSwitch').checked = agents.intent;
                        document.getElementById('salesSwitch').checked = agents.sales;
                        document.getElementById('techSwitch').checked = agents.tech;
                        document.getElementById('priceSwitch').checked = agents.price;
                        
                        // 更新UI状态
                        toggleAgentStatus('intentCard', agents.intent);
                        toggleAgentStatus('salesCard', agents.sales);
                        toggleAgentStatus('techCard', agents.tech);
                        toggleAgentStatus('priceCard', agents.price);
                    }
                    
                    if (settings.prompts) {
                        Object.assign(prompts, settings.prompts);
                    }
                } catch (e) {
                    console.error('解析本地配置出错:', e);
                }
            }
        });
});

// agent_settings.js - 客服Agent设置页面的交互逻辑
let currentAgentType = ''; // 当前正在编辑的Agent类型
let currentPromptField = ''; // 当前正在编辑的提示词字段名
let agentsConfig = {}; // 存储所有Agent的配置信息

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化加载所有Agent配置
    loadAgentSettings();
    
    // 绑定表单提交事件
    document.getElementById('agentSettingsForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveAllAgentSettings();
    });
});

// 从服务器加载Agent设置
function loadAgentSettings() {
    // 显示加载中提示
    showLoading(true);
    
    // 调用API获取所有Agent配置
    fetch('/api/agents/settings', {
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
            // 成功获取配置
            agentsConfig = data.body.agents;
            updateUIWithSettings(agentsConfig);
        } else {
            // 显示错误消息
            showToast('错误', data.message || '获取Agent配置失败', 'error');
        }
    })
    .catch(error => {
        console.error('获取Agent配置出错:', error);
        showToast('错误', '网络错误，请稍后重试', 'error');
    })
    .finally(() => {
        showLoading(false);
    });
}

// 使用配置数据更新UI
function updateUIWithSettings(agents) {
    if (!agents) return;
    
    // 更新各个Agent的开关状态和显示
    if (agents.intent) {
        document.getElementById('intentSwitch').checked = agents.intent.enabled;
        updateAgentStatusUI('intentCard', agents.intent.enabled);
    }
    
    if (agents.sales) {
        document.getElementById('salesSwitch').checked = agents.sales.enabled;
        updateAgentStatusUI('salesCard', agents.sales.enabled);
    }
    
    if (agents.tech) {
        document.getElementById('techSwitch').checked = agents.tech.enabled;
        updateAgentStatusUI('techCard', agents.tech.enabled);
    }
    
    if (agents.price) {
        document.getElementById('priceSwitch').checked = agents.price.enabled;
        updateAgentStatusUI('priceCard', agents.price.enabled);
    }
}

// 更新Agent卡片的状态显示
function updateAgentStatusUI(cardId, isEnabled) {
    const card = document.getElementById(cardId);
    const statusEl = document.getElementById(cardId.replace('Card', 'Status'));
    
    if (isEnabled) {
        card.classList.remove('disabled');
        statusEl.textContent = '已启用';
        statusEl.className = 'agent-status status-active';
    } else {
        card.classList.add('disabled');
        statusEl.textContent = '已禁用';
        statusEl.className = 'agent-status status-inactive';
    }
}

// 切换Agent的启用状态
function toggleAgentStatus(cardId, isEnabled) {
    // 获取Agent类型
    const agentType = cardId.replace('Card', '');
    
    // 更新UI显示
    updateAgentStatusUI(cardId, isEnabled);
    
    // 准备请求数据
    const requestData = {
        agent_type: agentType,
        enabled: isEnabled
    };
    
    // 调用API更新状态
    fetch('/api/agents/toggle-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            // 更新本地存储的配置
            if (agentsConfig[agentType]) {
                agentsConfig[agentType].enabled = isEnabled;
            }
            
            // 显示成功消息
            showToast('成功', `${isEnabled ? '启用' : '禁用'}成功`, 'success');
        } else {
            // 显示错误消息并回滚UI状态
            showToast('错误', data.message || '更新状态失败', 'error');
            document.getElementById(`${agentType}Switch`).checked = !isEnabled;
            updateAgentStatusUI(cardId, !isEnabled);
        }
    })
    .catch(error => {
        console.error('更新Agent状态出错:', error);
        showToast('错误', '网络错误，请稍后重试', 'error');
        
        // 回滚UI状态
        document.getElementById(`${agentType}Switch`).checked = !isEnabled;
        updateAgentStatusUI(cardId, !isEnabled);
    });
}

// 显示提示词编辑模态框
function showPromptModal(agentName, promptField) {
    // 设置当前正在编辑的Agent类型和提示词字段
    currentAgentType = promptField.replace('Prompt', '');
    currentPromptField = promptField;
    
    // 设置模态框标题
    document.getElementById('promptModalLabel').textContent = `编辑${agentName}Agent提示词`;
    
    // 获取并设置当前提示词内容
    const promptContent = agentsConfig[currentAgentType]?.prompt || '';
    document.getElementById('promptTextarea').value = promptContent;
    
    // 显示模态框
    const modal = new bootstrap.Modal(document.getElementById('promptModal'));
    modal.show();
}

// 保存提示词
function savePrompt() {
    const promptContent = document.getElementById('promptTextarea').value;
    
    // 准备请求数据
    const requestData = {
        agent_type: currentAgentType,
        prompt: promptContent
    };
    
    // 显示加载中提示
    showLoading(true);
    
    // 调用API保存提示词
    fetch('/api/agents/update-prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            // 更新本地存储的配置
            if (agentsConfig[currentAgentType]) {
                agentsConfig[currentAgentType].prompt = promptContent;
            }
            
            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('promptModal'));
            modal.hide();
            
            // 显示成功消息
            showToast('成功', '提示词已保存', 'success');
        } else {
            // 显示错误消息
            showToast('错误', data.message || '保存提示词失败', 'error');
        }
    })
    .catch(error => {
        console.error('保存提示词出错:', error);
        showToast('错误', '网络错误，请稍后重试', 'error');
    })
    .finally(() => {
        showLoading(false);
    });
}

// 保存所有Agent设置
function saveAllAgentSettings() {
    // 准备请求数据 - 从UI获取最新状态
    const settings = {
        intent: {
            enabled: document.getElementById('intentSwitch').checked,
            prompt: agentsConfig.intent?.prompt || ''
        },
        sales: {
            enabled: document.getElementById('salesSwitch').checked,
            prompt: agentsConfig.sales?.prompt || ''
        },
        tech: {
            enabled: document.getElementById('techSwitch').checked,
            prompt: agentsConfig.tech?.prompt || ''
        },
        price: {
            enabled: document.getElementById('priceSwitch').checked,
            prompt: agentsConfig.price?.prompt || ''
        }
    };
    
    // 显示加载中提示
    showLoading(true);
    
    // 调用API保存所有设置
    fetch('/api/agents/save-all-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'auth': localStorage.getItem('token') || ''
        },
        body: JSON.stringify({ agents: settings })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error === 0) {
            // 更新本地存储的配置
            agentsConfig = settings;
            
            // 显示成功消息
            showToast('成功', '所有配置已保存', 'success');
        } else {
            // 显示错误消息
            showToast('错误', data.message || '保存配置失败', 'error');
        }
    })
    .catch(error => {
        console.error('保存配置出错:', error);
        showToast('错误', '网络错误，请稍后重试', 'error');
    })
    .finally(() => {
        showLoading(false);
    });
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