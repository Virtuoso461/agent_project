#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支持流式输出的八字分析主程序
"""

import sys
import warnings
import os
from datetime import datetime
from agent_project.crew import AgentProject
from agent_project.streaming_callback import SimpleStreamingHandler

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run_with_streaming():
    """
    运行八字分析智能体团队（支持流式输出）
    """
    print("=== 八字分析智能体系统（流式输出版本）===")
    print("请输入您的出生信息进行八字分析：")

    # 获取用户输入
    name = input("请输入您的姓名：")
    gender = input("请输入您的性别（男/女）：")
    
    # 询问是否有准确的八字
    has_bazi = input("您是否已知准确的八字？(y/n)：").lower().strip()
    provided_bazi = None
    
    if has_bazi in ['y', 'yes', '是', '有']:
        provided_bazi = input("请输入您的八字（如：癸未甲寅戊午壬子）：").strip()
        if len(provided_bazi) != 8:
            print("⚠️  八字格式不正确，将使用出生时间计算")
            provided_bazi = None

    # 获取出生日期
    try:
        birth_year = int(input("请输入出生年份（如：1990）："))
        birth_month = int(input("请输入出生月份（如：5）："))
        birth_day = int(input("请输入出生日期（如：15）："))
        birth_hour = int(input("请输入出生小时（24小时制，如：14）："))
        birth_minute = int(input("请输入出生分钟（如：30）：") or "0")

        # 验证输入
        if not (1900 <= birth_year <= 2100):
            raise ValueError("年份应在1900-2100之间")
        if not (1 <= birth_month <= 12):
            raise ValueError("月份应在1-12之间")
        if not (1 <= birth_day <= 31):
            raise ValueError("日期应在1-31之间")
        if not (0 <= birth_hour <= 23):
            raise ValueError("小时应在0-23之间")
        if not (0 <= birth_minute <= 59):
            raise ValueError("分钟应在0-59之间")
        if gender not in ['男', '女']:
            raise ValueError("性别请输入'男'或'女'")

    except ValueError as e:
        print(f"输入错误：{e}")
        return

    # 获取出生地点
    birth_place = input("请输入出生地点（可选）：") or "未指定"

    # 准备输入数据（匹配任务配置的期望格式）
    inputs = {
        'name': name,
        'gender': gender,
        'birth_date': f"{birth_year}年{birth_month}月{birth_day}日",
        'birth_time': f"{birth_hour}时{birth_minute:02d}分",
        'birth_place': birth_place,
        'provided_bazi': provided_bazi or "",
        # 同时保留详细的时间信息供工具使用
        'birth_year': birth_year,
        'birth_month': birth_month,
        'birth_day': birth_day,
        'birth_hour': birth_hour,
        'birth_minute': birth_minute
    }

    print(f"\n🎯 开始为 {name}（{gender}）进行八字分析...")
    print(f"📅 出生时间：{birth_year}年{birth_month}月{birth_day}日{birth_hour}时{birth_minute:02d}分")
    if provided_bazi:
        print(f"🔮 使用提供的八字：{provided_bazi}")
    print(f"📍 出生地点：{birth_place}")
    print("=" * 60)

    try:
        # 创建流式处理器
        stream_handler = SimpleStreamingHandler()
        
        # 重定向标准输出以捕获流式内容
        original_stdout = sys.stdout
        
        print("\n🚀 开始分析，请稍候...")
        print("=" * 60)
        
        # 执行分析
        result = AgentProject().crew().kickoff(inputs=inputs)
        
        # 恢复标准输出
        sys.stdout = original_stdout
        
        print("\n" + "=" * 60)
        print("✅ 八字分析完成！")
        print("=" * 60)
        
        # 显示最终结果
        if hasattr(result, 'raw'):
            print("\n📋 最终分析报告：")
            print("-" * 40)
            print(result.raw)
        else:
            print("\n📋 最终分析报告：")
            print("-" * 40)
            print(str(result))
            
        return result
        
    except Exception as e:
        # 恢复标准输出
        sys.stdout = original_stdout
        print(f"\n❌ 分析过程中出现错误：{e}")
        import traceback
        traceback.print_exc()
        raise Exception(f"An error occurred while running the crew: {e}")


def test_streaming():
    """测试流式输出功能"""
    print("=== 流式输出测试 ===")
    
    # 使用测试数据（匹配任务配置的期望格式）
    inputs = {
        'name': '邱家鹏',
        'gender': '男',
        'birth_date': '2003年2月13日',
        'birth_time': '23时55分',
        'birth_place': '福建厦门',
        'provided_bazi': '癸未甲寅戊午壬子',
        # 同时保留详细的时间信息供工具使用
        'birth_year': 2003,
        'birth_month': 2,
        'birth_day': 13,
        'birth_hour': 23,
        'birth_minute': 55
    }
    
    print(f"🎯 测试用户：{inputs['name']}（{inputs['gender']}）")
    print(f"📅 出生时间：{inputs['birth_year']}年{inputs['birth_month']}月{inputs['birth_day']}日{inputs['birth_hour']}时{inputs['birth_minute']:02d}分")
    print(f"🔮 八字：{inputs['provided_bazi']}")
    print("=" * 60)
    
    try:
        result = AgentProject().crew().kickoff(inputs=inputs)
        print("\n✅ 测试完成！")
        return result
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_streaming()
    else:
        run_with_streaming()
