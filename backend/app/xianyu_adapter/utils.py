import json
import subprocess
from functools import partial
import os
from pathlib import Path
from loguru import logger

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

def load_xianyu_js():
    """加载闲鱼JS工具脚本"""
    try:
        js_path = Path(__file__).parent.parent.parent.parent / 'static' / 'xianyu_js_version_2.js'
        if not js_path.exists():
            # 尝试另一个可能的路径
            js_path = Path(os.getcwd()) / 'static' / 'xianyu_js_version_2.js'
        
        if not js_path.exists():
            logger.error(f"找不到闲鱼JS工具脚本: {js_path}")
            raise FileNotFoundError(f"找不到闲鱼JS工具脚本: {js_path}")
            
        with open(js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
            
        return execjs.compile(js_code)
    except Exception as e:
        logger.error(f"加载闲鱼JS工具脚本失败: {e}")
        raise

# 加载JS脚本
try:
    xianyu_js = load_xianyu_js()
except Exception as e:
    logger.error(f"初始化闲鱼JS工具脚本失败: {e}")
    # 在实际运行时，可能需要抛出异常或采取其他恢复措施
    xianyu_js = None

def trans_cookies(cookies_str):
    """
    将Cookie字符串转换为字典格式
    
    Args:
        cookies_str: Cookie字符串，格式为"name1=value1; name2=value2"
        
    Returns:
        dict: Cookie字典
    """
    cookies = dict()
    for i in cookies_str.split("; "):
        try:
            cookies[i.split('=')[0]] = '='.join(i.split('=')[1:])
        except:
            continue
    return cookies


def generate_mid():
    """
    生成消息ID
    
    Returns:
        str: 消息ID
    """
    if xianyu_js is None:
        logger.error("闲鱼JS工具脚本未初始化")
        return "error_mid"
        
    mid = xianyu_js.call('generate_mid')
    return mid

def generate_uuid():
    """
    生成UUID
    
    Returns:
        str: UUID
    """
    if xianyu_js is None:
        logger.error("闲鱼JS工具脚本未初始化")
        return "error_uuid"
        
    uuid = xianyu_js.call('generate_uuid')
    return uuid

def generate_device_id(user_id):
    """
    根据用户ID生成设备ID
    
    Args:
        user_id: 用户ID
        
    Returns:
        str: 设备ID
    """
    if xianyu_js is None:
        logger.error("闲鱼JS工具脚本未初始化")
        return "error_device_id"
        
    device_id = xianyu_js.call('generate_device_id', user_id)
    return device_id

def generate_sign(t, token, data):
    """
    生成签名
    
    Args:
        t: 时间戳
        token: 令牌
        data: 数据
        
    Returns:
        str: 签名
    """
    if xianyu_js is None:
        logger.error("闲鱼JS工具脚本未初始化")
        return "error_sign"
        
    sign = xianyu_js.call('generate_sign', t, token, data)
    return sign

def decrypt(data):
    """
    解密数据
    
    Args:
        data: 加密数据
        
    Returns:
        str: 解密后的数据
    """
    if xianyu_js is None:
        logger.error("闲鱼JS工具脚本未初始化")
        return "{}"
        
    res = xianyu_js.call('decrypt', data)
    return res 