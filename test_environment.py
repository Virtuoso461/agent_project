#!/usr/bin/env python3
"""
环境测试脚本
测试项目环境是否正确配置
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """测试环境配置"""
    print("=== 环境测试开始 ===")
    
    # 1. 测试Python版本
    print(f"Python版本: {sys.version}")
    
    # 2. 测试环境变量加载
    load_dotenv()
    print("✓ 环境变量文件加载成功")
    
    # 3. 检查关键环境变量
    deep_seek_key = os.getenv("DEEP_SEEK_KEY")
    deep_seek_url = os.getenv("DEEP_SEEK_URL")
    
    if deep_seek_key and deep_seek_key != "your_deepseek_api_key_here":
        print("✓ DEEP_SEEK_KEY 已配置")
    else:
        print("⚠ DEEP_SEEK_KEY 需要配置实际的API密钥")
    
    if deep_seek_url:
        print(f"✓ DEEP_SEEK_URL: {deep_seek_url}")
    else:
        print("⚠ DEEP_SEEK_URL 未配置")
    
    # 4. 测试crewAI导入
    try:
        from crewai import Agent, Crew, Process, Task, LLM
        print("✓ crewAI 导入成功")
    except ImportError as e:
        print(f"✗ crewAI 导入失败: {e}")
        return False
    
    # 5. 测试项目模块导入
    try:
        from agent_project.crew import AgentProject
        print("✓ 项目模块导入成功")
    except ImportError as e:
        print(f"✗ 项目模块导入失败: {e}")
        return False
    
    # 6. 测试配置文件
    try:
        project = AgentProject()
        print("✓ AgentProject 实例化成功")
    except Exception as e:
        print(f"✗ AgentProject 实例化失败: {e}")
        return False
    
    print("=== 环境测试完成 ===")
    return True

def test_basic_functionality():
    """测试基本功能（不调用API）"""
    print("\n=== 基本功能测试 ===")
    
    try:
        from agent_project.crew import AgentProject
        
        # 创建项目实例
        project = AgentProject()
        
        # 测试智能体创建
        bazi_agent = project.bazi_calculator_agent()
        print("✓ 八字排盘智能体创建成功")
        
        wuxing_agent = project.wuxing_analyzer_agent()
        print("✓ 五行分析智能体创建成功")
        
        # 测试任务创建
        bazi_task = project.calculate_bazi_task()
        print("✓ 八字排盘任务创建成功")
        
        # 测试团队创建
        crew = project.crew()
        print("✓ 智能体团队创建成功")
        
        print("=== 基本功能测试完成 ===")
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

if __name__ == "__main__":
    # 运行环境测试
    env_ok = test_environment()
    
    if env_ok:
        # 运行基本功能测试
        func_ok = test_basic_functionality()
        
        if func_ok:
            print("\n🎉 环境构建成功！项目已准备就绪。")
            print("\n📝 下一步操作：")
            print("1. 在 .env 文件中配置您的 DeepSeek API 密钥")
            print("2. 运行 'uv run agent_project' 开始使用八字分析系统")
        else:
            print("\n❌ 基本功能测试失败，请检查配置")
    else:
        print("\n❌ 环境测试失败，请检查依赖安装")
