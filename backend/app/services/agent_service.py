from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path
from loguru import logger

class AgentService:
    """
    Agent服务 - 负责Agent设置的CRUD操作
    """
    def __init__(self):
        # 设置文件存储路径
        self.config_file = Path("backend/data/agent_settings.json")
        # 确保包含配置文件的目录存在
        if not self.config_file.parent.exists():
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
        # 如果配置文件不存在，创建默认配置
        if not self.config_file.exists():
            self._create_default_config()
            
    def _create_default_config(self):
        """创建默认的Agent配置"""
        default_config = {
            "intent": {
                "enabled": True,
                "prompt": "你是一个分类专家，负责分析客户意图，并将消息分类为以下几种类型:\n1. 咨询类：用户询问产品信息、价格、功能等\n2. 投诉类：用户表达不满、抱怨或投诉\n3. 售后类：用户询问退换货、维修等售后服务\n4. 技术类：用户询问产品使用方法、技术问题等\n5. 价格类：用户询问价格、折扣、优惠等\n\n请根据用户消息，分析意图并返回一个标签。"
            },
            "sales": {
                "enabled": True,
                "prompt": "你是一个专业的电商客服，负责回答用户关于产品、订单和一般服务的问题。你的回答应当：\n1. 简洁明了，直击要点\n2. 语气友好，有耐心\n3. 提供准确信息，不夸大产品效果\n4. 在必要时引导用户完成购买\n5. 使用礼貌用语，如\"您好\"、\"感谢您的咨询\"等\n\n请根据商品信息和用户问题，提供专业、有帮助的回答。"
            },
            "tech": {
                "enabled": True,
                "prompt": "你是一位专业的技术支持专家，负责解决用户在使用产品过程中遇到的各种技术问题。你应当：\n1. 提供清晰的步骤指导\n2. 使用简单易懂的语言解释技术概念\n3. 在可能的情况下提供多种解决方案\n4. 询问详细信息以便更准确地诊断问题\n5. 保持专业耐心的态度\n\n请根据用户描述的问题，提供专业的技术支持。"
            },
            "price": {
                "enabled": True,
                "prompt": "你是一位专业的销售顾问，负责处理用户关于价格、折扣和促销的咨询。你的回答应当：\n1. 强调产品价值而非仅关注价格\n2. 介绍当前可用的优惠和促销活动\n3. 建议最适合用户需求的产品/套餐\n4. 适当引导用户完成购买决策\n5. 使用专业且有说服力的语言\n\n请根据用户的价格咨询，提供有价值且有说服力的回答。"
            }
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
        logger.info(f"已创建默认Agent配置文件: {self.config_file}")
    
    def _load_config(self) -> Dict[str, Any]:
        """从文件加载配置"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载Agent配置失败: {str(e)}")
            # 如果加载失败，创建并返回默认配置
            self._create_default_config()
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
    
    def _save_config(self, config: Dict[str, Any]):
        """保存配置到文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            logger.info("Agent配置已保存")
        except Exception as e:
            logger.error(f"保存Agent配置失败: {str(e)}")
            raise
    
    def get_all_agent_settings(self) -> Dict[str, Any]:
        """获取所有Agent的设置"""
        return self._load_config()
    
    def get_agent_settings(self, agent_type: str) -> Optional[Dict[str, Any]]:
        """获取指定Agent的设置"""
        config = self._load_config()
        return config.get(agent_type)
    
    def update_agent_status(self, agent_type: str, enabled: bool):
        """更新Agent的启用状态"""
        config = self._load_config()
        if agent_type not in config:
            raise ValueError(f"无效的Agent类型: {agent_type}")
        
        config[agent_type]["enabled"] = enabled
        self._save_config(config)
        logger.info(f"已更新Agent {agent_type} 的状态为 {enabled}")
    
    def update_agent_prompt(self, agent_type: str, prompt: str):
        """更新Agent的提示词"""
        config = self._load_config()
        if agent_type not in config:
            raise ValueError(f"无效的Agent类型: {agent_type}")
        
        config[agent_type]["prompt"] = prompt
        self._save_config(config)
        logger.info(f"已更新Agent {agent_type} 的提示词")
    
    def save_all_agent_settings(self, agent_settings: Dict[str, Any]):
        """保存所有Agent的设置"""
        # 获取当前配置作为基础
        current_config = self._load_config()
        
        # 更新配置
        for agent_type, settings in agent_settings.items():
            if agent_type in current_config:
                current_config[agent_type]["enabled"] = settings.enabled
                current_config[agent_type]["prompt"] = settings.prompt
        
        # 保存更新后的配置
        self._save_config(current_config)
        logger.info("已保存所有Agent配置") 