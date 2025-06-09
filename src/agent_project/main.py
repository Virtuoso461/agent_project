#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agent_project.crew import AgentProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    运行八字分析智能体团队
    """
    print("=== 八字分析智能体系统 ===")
    print("请输入您的出生信息进行八字分析：")

    # 获取用户输入
    name = input("请输入您的姓名：")
    gender = input("请输入您的性别（男/女）：")

    # 获取出生日期
    try:
        birth_year = int(input("请输入出生年份（如：1990）："))
        birth_month = int(input("请输入出生月份（如：5）："))
        birth_day = int(input("请输入出生日期（如：15）："))
        birth_hour = int(input("请输入出生小时（24小时制，如：14）："))

        # 验证输入
        if not (1900 <= birth_year <= 2100):
            raise ValueError("年份应在1900-2100之间")
        if not (1 <= birth_month <= 12):
            raise ValueError("月份应在1-12之间")
        if not (1 <= birth_day <= 31):
            raise ValueError("日期应在1-31之间")
        if not (0 <= birth_hour <= 23):
            raise ValueError("小时应在0-23之间")
        if gender not in ['男', '女']:
            raise ValueError("性别请输入'男'或'女'")

    except ValueError as e:
        print(f"输入错误：{e}")
        return

    # 准备输入数据
    inputs = {
        'name': name,
        'gender': gender,
        'birth_date': f"{birth_year}年{birth_month}月{birth_day}日",
        'birth_time': f"{birth_hour}时",
        'birth_place': "未指定"  # 可选字段
    }

    print(f"\n开始为 {name}（{gender}）进行八字分析...")
    print(f"出生时间：{birth_year}年{birth_month}月{birth_day}日{birth_hour}时")
    print("=" * 50)

    try:
        result = AgentProject().crew().kickoff(inputs=inputs)
        print("\n八字分析完成！")
        return result
    except Exception as e:
        print(f"分析过程中出现错误：{e}")
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentProject().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgentProject().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        AgentProject().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
