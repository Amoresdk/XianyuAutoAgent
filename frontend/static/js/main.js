// 菜单配置
const menuConfig = {
    'settings.html': {
        title: '系统设置',
        subMenu: [
            { title: '参数配置', url: 'model_settings.html', icon: 'fas fa-microchip' },
            { title: 'Agent配置', url: 'agent_settings.html', icon: 'fas fa-user-tie' },
            { title: '敏感词过滤', url: 'filter_settings.html', icon: 'fas fa-filter' }
        ]
    },
    'conversation.html': {
        title: '会话管理',
        subMenu: [
            { title: '会话列表', url: 'conversation.html', icon: 'fas fa-list' }
        ]
    },
    'logs.html': {
        title: '系统日志',
        subMenu: [
            { title: '最新日志', url: 'logs.html', icon: 'fas fa-clock' },
            { title: '错误日志', url: 'error_logs.html', icon: 'fas fa-exclamation-triangle' }
        ]
    }
};

// 当前一级菜单和二级菜单
let currentMainMenu = 'conversation.html';
let currentSubMenu = '';

function changeFrame(url, navLink) {
    // 更新内容框架
    document.getElementById('contentFrame').src = 'pages/' + url;
    
    // 如果点击的是主菜单
    if (navLink) {
        // 更新活动导航项
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => link.classList.remove('active'));
        navLink.classList.add('active');
        
        // 更新当前主菜单
        for (const key in menuConfig) {
            if (url === key) {
                currentMainMenu = key;
                break;
            }
        }
        
        // 如果点击的是系统设置，默认打开模型配置页面
        if (url === 'settings.html') {
            document.getElementById('contentFrame').src = 'pages/model_settings.html';
        }
        
        // 更新二级菜单
        updateSubNav();
    } else {
        // 如果是点击二级菜单，更新二级菜单活动状态
        updateSubNavActiveState(url);
    }
}

function updateSubNav() {
    const subNavContainer = document.getElementById('subNavContainer');
    subNavContainer.innerHTML = '';
    
    if (menuConfig[currentMainMenu] && menuConfig[currentMainMenu].subMenu) {
        const subMenuItems = menuConfig[currentMainMenu].subMenu;
        
        subMenuItems.forEach(item => {
            const link = document.createElement('a');
            link.href = '#';
            link.className = 'top-nav-item';
            if (item.url === document.getElementById('contentFrame').src.split('/').pop()) {
                link.classList.add('active');
                currentSubMenu = item.url;
            }
            link.innerHTML = `<i class="${item.icon} me-2"></i>${item.title}`;
            link.onclick = function(e) {
                e.preventDefault();
                changeFrame(item.url);
            };
            subNavContainer.appendChild(link);
        });
    }
}

function updateSubNavActiveState(url) {
    const subNavItems = document.querySelectorAll('.top-nav-item');
    subNavItems.forEach(item => {
        item.classList.remove('active');
        if (item.textContent.includes(getMenuTitleByUrl(url))) {
            item.classList.add('active');
        }
    });
    currentSubMenu = url;
}

function getMenuTitleByUrl(url) {
    for (const key in menuConfig) {
        const subMenu = menuConfig[key].subMenu;
        for (const item of subMenu) {
            if (item.url === url) {
                return item.title;
            }
        }
    }
    return '';
}

// 初始化二级菜单
document.addEventListener('DOMContentLoaded', function() {
    updateSubNav();
    
    // 监听iframe加载完成事件，更新二级菜单活动状态
    document.getElementById('contentFrame').onload = function() {
        const url = this.contentWindow.location.pathname.split('/').pop();
        updateSubNavActiveState(url);
    };
}); 