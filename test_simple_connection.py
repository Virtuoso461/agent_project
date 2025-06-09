#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的DeepSeek API连接测试
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_env_vars():
    """测试环境变量"""
    print("=" * 50)
    print("🔧 环境变量检查")
    print("=" * 50)
    
    deep_seek_key = os.getenv("DEEP_SEEK_KEY")
    deep_seek_url = os.getenv("DEEP_SEEK_URL")
    
    print(f"DEEP_SEEK_KEY: {'✅ 已设置' if deep_seek_key else '❌ 未设置'}")
    print(f"DEEP_SEEK_URL: {'✅ 已设置' if deep_seek_url else '❌ 未设置'}")
    
    if deep_seek_key:
        print(f"API Key前缀: {deep_seek_key[:10]}...")
    if deep_seek_url:
        print(f"API URL: {deep_seek_url}")
    
    return deep_seek_key, deep_seek_url

def test_openai_client():
    """测试OpenAI客户端连接"""
    print("\n" + "=" * 50)
    print("🌐 OpenAI客户端连接测试")
    print("=" * 50)
    
    try:
        from openai import OpenAI
        
        deep_seek_key = os.getenv("DEEP_SEEK_KEY")
        deep_seek_url = os.getenv("DEEP_SEEK_URL")
        
        if not deep_seek_key or not deep_seek_url:
            print("❌ 环境变量未设置")
            return False
            
        client = OpenAI(
            api_key=deep_seek_key,
            base_url=deep_seek_url
        )
        
        print("✅ OpenAI客户端创建成功")
        
        # 测试简单的API调用
        print("🔄 测试API调用...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": "你好，请简单回复一下"}
            ],
            max_tokens=50,
            timeout=30  # 设置30秒超时
        )
        
        print("✅ API调用成功")
        print(f"回复: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_crewai_llm():
    """测试CrewAI LLM配置"""
    print("\n" + "=" * 50)
    print("🤖 CrewAI LLM配置测试")
    print("=" * 50)
    
    try:
        from crewai import LLM
        
        deep_seek_key = os.getenv("DEEP_SEEK_KEY")
        deep_seek_url = os.getenv("DEEP_SEEK_URL")
        
        if not deep_seek_key or not deep_seek_url:
            print("❌ 环境变量未设置")
            return False
            
        # 尝试不同的模型配置方式
        print("🔄 测试CrewAI LLM配置...")
        
        # 方式1：使用openai/前缀
        try:
            llm1 = LLM(
                model="openai/deepseek-chat",
                api_key=deep_seek_key,
                base_url=deep_seek_url
            )
            print("✅ 方式1成功: openai/deepseek-chat")
        except Exception as e:
            print(f"❌ 方式1失败: {e}")
        
        # 方式2：直接使用模型名
        try:
            llm2 = LLM(
                model="deepseek-chat",
                api_key=deep_seek_key,
                base_url=deep_seek_url
            )
            print("✅ 方式2成功: deepseek-chat")
        except Exception as e:
            print(f"❌ 方式2失败: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ CrewAI LLM配置失败: {e}")
        return False

if __name__ == "__main__":
    print("🔍 DeepSeek API连接诊断工具")
    print("=" * 50)
    
    # 测试环境变量
    env_ok = test_env_vars()
    
    if not all(env_ok):
        print("\n❌ 环境变量配置有问题，请检查.env文件")
        sys.exit(1)
    
    # 测试OpenAI客户端
    openai_ok = test_openai_client()
    
    # 测试CrewAI LLM
    crewai_ok = test_crewai_llm()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    print(f"环境变量: {'✅' if all(env_ok) else '❌'}")
    print(f"OpenAI客户端: {'✅' if openai_ok else '❌'}")
    print(f"CrewAI LLM: {'✅' if crewai_ok else '❌'}")
    
    if all([all(env_ok), openai_ok, crewai_ok]):
        print("\n🎉 所有测试通过！可以运行完整的八字分析程序")
    else:
        print("\n⚠️ 存在问题，需要修复后再运行完整程序")
