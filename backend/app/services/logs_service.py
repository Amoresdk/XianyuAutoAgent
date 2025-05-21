from typing import Dict, Any, List, Optional
import os
from pathlib import Path
from loguru import logger
import re
from datetime import datetime

class LogsService:
    """
    日志服务 - 负责日志的读取和分析
    """
    def __init__(self, log_dir: str = "logs"):
        # 设置日志目录
        self.log_dir = Path(log_dir)
        # 确保日志目录存在
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建日志目录: {self.log_dir}")
    
    def get_log_files(self) -> List[Path]:
        """获取所有日志文件列表"""
        try:
            log_files = list(self.log_dir.glob("*.log"))
            return sorted(log_files, key=lambda x: x.stat().st_mtime, reverse=True)
        except Exception as e:
            logger.error(f"获取日志文件列表失败: {str(e)}")
            return []
    
    def get_latest_log_file(self) -> Optional[Path]:
        """获取最新的日志文件"""
        log_files = self.get_log_files()
        return log_files[0] if log_files else None
    
    def get_error_log_file(self) -> Optional[Path]:
        """获取错误日志文件"""
        # 优先查找error.log或errors.log
        for pattern in ["error.log", "errors.log"]:
            error_log = self.log_dir / pattern
            if error_log.exists():
                return error_log
        
        # 如果没有专门的错误日志文件，返回最新的普通日志文件
        return self.get_latest_log_file()
    
    def read_latest_log_lines(self, line_count: int = 100) -> List[str]:
        """
        读取最新的日志行
        
        参数:
            line_count: 要读取的最大行数
            
        返回:
            日志行列表
        """
        try:
            log_file = self.get_latest_log_file()
            if not log_file:
                return ["没有找到日志文件"]
            
            # 读取日志文件的最后N行
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                
            # 返回最后line_count行
            return [line.rstrip() for line in lines[-line_count:] if line.strip()]
        except Exception as e:
            logger.error(f"读取最新日志失败: {str(e)}")
            return [f"读取日志出错: {str(e)}"]
    
    def read_error_log_lines(self, line_count: int = 100) -> List[str]:
        """
        读取错误日志行
        
        参数:
            line_count: 要读取的最大行数
            
        返回:
            错误日志行列表
        """
        try:
            log_file = self.get_error_log_file()
            if not log_file:
                return ["没有找到错误日志文件"]
            
            # 如果是专门的错误日志文件，直接读取
            if log_file.name.lower().startswith("error"):
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                return [line.rstrip() for line in lines[-line_count:] if line.strip()]
            
            # 否则从普通日志文件中筛选错误日志
            all_lines = self.read_latest_log_lines(line_count * 5)  # 读取更多行以确保有足够的错误日志
            error_lines = [line for line in all_lines if re.search(r"error|exception|traceback|fail", line, re.IGNORECASE)]
            
            # 返回最多line_count行错误日志
            return error_lines[-line_count:]
        except Exception as e:
            logger.error(f"读取错误日志失败: {str(e)}")
            return [f"读取错误日志出错: {str(e)}"]
    
    def get_dummy_logs(self) -> List[str]:
        """获取示例日志数据（用于开发测试）"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [
            f"{current_time} [INFO] 服务启动成功，监听端口: 8080",
            f"{current_time} [INFO] 用户登录: admin_user (IP: 192.168.1.100)",
            f"{current_time} [DEBUG] 加载配置文件: config/app.yaml",
            f"{current_time} [ERROR] 请求闲鱼API失败，错误代码: 401",
            f"{current_time} [INFO] 重试请求...",
            f"{current_time} [INFO] 请求成功，获取到5条新消息"
        ]
    
    def get_dummy_error_logs(self) -> List[str]:
        """获取示例错误日志数据（用于开发测试）"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [
            f"{current_time} [ERROR] 请求闲鱼API失败，错误代码: 401",
            f"{current_time} [ERROR] 连接超时: https://api.example.com/v1/messages",
            f"{current_time} [ERROR] 无法解析JSON响应: SyntaxError: Unexpected token }} in JSON at position 432",
            f"{current_time} [ERROR] 用户认证失败，无效的token"
        ] 