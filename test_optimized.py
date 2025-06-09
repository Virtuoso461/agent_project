#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化后的八字分析系统测试脚本
专业化、精细化、高度专业的命理分析
"""

import sys
import os
import io
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_optimized_bazi_analysis():
    """测试优化后的八字分析功能"""
    print("=" * 60)
    print("🔮 专业八字命理分析系统 🔮")
    print("二十余年经验·权威命理团队·精准预测")
    print("=" * 60)

    # 检查环境变量
    deep_seek_key = os.getenv("DEEP_SEEK_KEY")
    deep_seek_url = os.getenv("DEEP_SEEK_URL")

    if not deep_seek_key:
        print("❌ 缺少DEEP_SEEK_KEY环境变量")
        return
    if not deep_seek_url:
        print("❌ 缺少DEEP_SEEK_URL环境变量")
        return

    print(f"✅ 系统环境检查通过")
    print(f"📡 API服务地址: {deep_seek_url}")
    print(f"⏰ 当前时间: 2025年6月（乙巳年午月）")

    # 使用用户提供的八字数据
    test_inputs = {
        'name': '特定求测者',
        'gender': '女',
        'birth_date': '2002年1月8日',
        'birth_time': '16时03分',
        'birth_place': '上海徐汇',
        'provided_bazi': '辛巳辛丑丙子丙申'  # 用户提供的准确八字
    }

    print("\n📋 求测者信息：")
    print("-" * 40)
    print(f"   姓名: {test_inputs['name']}")
    print(f"   性别: {test_inputs['gender']}")
    print(f"   出生日期: {test_inputs['birth_date']}")
    print(f"   出生时间: {test_inputs['birth_time']}")
    print(f"   出生地点: {test_inputs['birth_place']}")
    print(f"   八字: {test_inputs['provided_bazi']}")

    print("\n🎯 开始专业命理分析...")
    print("📊 分析团队：资深八字大师 + 五行命理宗师 + 性格解析专家 + 运势预测大师 + 人生智慧导师")
    print("=" * 60)

    try:
        from agent_project.crew import AgentProject

        # 创建并运行专业命理分析团队
        crew = AgentProject().crew()
        result = crew.kickoff(inputs=test_inputs)

        print("\n" + "=" * 60)
        print("✅ 专业命理分析完成！")
        print("=" * 60)

        print("\n📜 完整分析报告：")
        print("-" * 60)
        if hasattr(result, 'raw'):
            print(result.raw)
        else:
            print(str(result))

        print("\n" + "=" * 60)
        print("🙏 感谢您选择我们的专业命理服务")
        print("💫 愿您前程似锦，吉祥如意")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 分析过程中出现异常：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_optimized_bazi_analysis()
    print("\n🎉 测试完成！")
