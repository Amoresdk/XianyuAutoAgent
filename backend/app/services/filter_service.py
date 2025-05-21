from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path
from loguru import logger

class FilterService:
    """
    敏感词过滤服务 - 负责敏感词的增删改查操作
    """
    def __init__(self):
        # 设置文件存储路径
        self.config_file = Path("backend/data/filter_words.json")
        # 确保包含配置文件的目录存在
        if not self.config_file.parent.exists():
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
        # 如果配置文件不存在，创建默认配置
        if not self.config_file.exists():
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认的敏感词配置"""
        default_words = [
            "敏感词1",
            "违禁词",
            "色情",
            "赌博",
            "政治敏感"
        ]
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(default_words, f, ensure_ascii=False, indent=4)
        logger.info(f"已创建默认敏感词配置文件: {self.config_file}")
    
    def _load_words(self) -> List[str]:
        """从文件加载敏感词列表"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载敏感词列表失败: {str(e)}")
            # 如果加载失败，创建并返回默认配置
            self._create_default_config()
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
    
    def _save_words(self, words: List[str]):
        """保存敏感词列表到文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(words, f, ensure_ascii=False, indent=4)
            logger.info("敏感词列表已保存")
        except Exception as e:
            logger.error(f"保存敏感词列表失败: {str(e)}")
            raise
    
    def get_all_words(self) -> List[str]:
        """获取所有敏感词"""
        return self._load_words()
    
    def word_exists(self, word: str) -> bool:
        """检查敏感词是否存在"""
        words = self._load_words()
        return word in words
    
    def add_word(self, word: str):
        """添加敏感词"""
        words = self._load_words()
        if word not in words:
            words.append(word)
            self._save_words(words)
            logger.info(f"已添加敏感词: {word}")
        else:
            logger.warning(f"敏感词已存在: {word}")
    
    def delete_word(self, word: str):
        """删除敏感词"""
        words = self._load_words()
        if word in words:
            words.remove(word)
            self._save_words(words)
            logger.info(f"已删除敏感词: {word}")
        else:
            logger.warning(f"敏感词不存在: {word}")
    
    def clear_all_words(self):
        """清空所有敏感词"""
        self._save_words([])
        logger.info("已清空所有敏感词")
    
    def check_text(self, text: str) -> Dict[str, Any]:
        """
        检查文本中是否包含敏感词
        
        返回:
            Dict: {
                "has_sensitive": bool,  # 是否包含敏感词
                "matched_words": List[str]  # 匹配到的敏感词列表
            }
        """
        words = self._load_words()
        matched_words = []
        
        for word in words:
            if word in text:
                matched_words.append(word)
        
        return {
            "has_sensitive": len(matched_words) > 0,
            "matched_words": matched_words
        } 