#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流式输出回调处理器
"""

import sys
from typing import Any, Dict, List, Optional
from crewai.agent import Agent
from crewai.task import Task


class StreamingCallback:
    """流式输出回调处理器"""
    
    def __init__(self):
        self.current_agent = None
        self.current_task = None
        
    def on_agent_start(self, agent: Agent, **kwargs):
        """智能体开始工作时的回调"""
        self.current_agent = agent
        print(f"\n🤖 【{agent.role}】开始工作...")
        print(f"📋 目标: {agent.goal}")
        print("-" * 50)
        sys.stdout.flush()
        
    def on_agent_end(self, agent: Agent, **kwargs):
        """智能体完成工作时的回调"""
        print(f"\n✅ 【{agent.role}】工作完成")
        print("=" * 50)
        sys.stdout.flush()
        
    def on_task_start(self, task: Task, **kwargs):
        """任务开始时的回调"""
        self.current_task = task
        print(f"\n📝 开始执行任务: {task.description[:50]}...")
        sys.stdout.flush()
        
    def on_task_end(self, task: Task, **kwargs):
        """任务完成时的回调"""
        print(f"\n✅ 任务完成")
        sys.stdout.flush()
        
    def on_tool_start(self, tool_name: str, tool_input: Dict[str, Any], **kwargs):
        """工具开始执行时的回调"""
        print(f"\n🔧 使用工具: {tool_name}")
        # 只显示关键参数，避免输出过多信息
        if 'name' in tool_input:
            print(f"   姓名: {tool_input['name']}")
        if 'provided_bazi' in tool_input and tool_input['provided_bazi']:
            print(f"   八字: {tool_input['provided_bazi']}")
        sys.stdout.flush()
        
    def on_tool_end(self, tool_name: str, tool_output: str, **kwargs):
        """工具执行完成时的回调"""
        print(f"✅ 工具 {tool_name} 执行完成")
        # 显示工具输出的前几行
        lines = tool_output.split('\n')[:3]
        for line in lines:
            if line.strip():
                print(f"   {line}")
        if len(tool_output.split('\n')) > 3:
            print("   ...")
        sys.stdout.flush()
        
    def on_llm_start(self, prompt: str, **kwargs):
        """LLM开始生成时的回调"""
        print(f"\n🧠 AI思考中...")
        sys.stdout.flush()
        
    def on_llm_new_token(self, token: str, **kwargs):
        """LLM生成新token时的回调（流式输出）"""
        # 实时输出每个token
        print(token, end='', flush=True)
        
    def on_llm_end(self, response: str, **kwargs):
        """LLM生成完成时的回调"""
        print(f"\n💭 AI思考完成")
        sys.stdout.flush()
        
    def on_chain_start(self, inputs: Dict[str, Any], **kwargs):
        """链开始时的回调"""
        pass
        
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs):
        """链结束时的回调"""
        pass
        
    def on_chain_error(self, error: Exception, **kwargs):
        """链出错时的回调"""
        print(f"\n❌ 执行出错: {error}")
        sys.stdout.flush()


class SimpleStreamingHandler:
    """简化的流式处理器"""
    
    def __init__(self):
        self.buffer = ""
        
    def write(self, text: str):
        """写入文本并实时输出"""
        if text and text.strip():
            print(text, end='', flush=True)
            self.buffer += text
            
    def flush(self):
        """刷新缓冲区"""
        sys.stdout.flush()
        
    def get_content(self) -> str:
        """获取所有内容"""
        return self.buffer
