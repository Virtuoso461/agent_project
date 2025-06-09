from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
from datetime import date


class BaziCalculatorInput(BaseModel):
    """八字计算工具输入模式"""
    name: str = Field(..., description="姓名")
    birth_year: int = Field(..., description="出生年份（公历）")
    birth_month: int = Field(..., description="出生月份（公历）")
    birth_day: int = Field(..., description="出生日期（公历）")
    birth_hour: int = Field(..., description="出生小时（24小时制）")
    birth_minute: int = Field(0, description="出生分钟")
    gender: str = Field(..., description="性别：男/女")
    birth_place: str = Field("", description="出生地点")
    provided_bazi: Optional[str] = Field(None, description="用户提供的准确八字（如：癸未甲寅戊午壬子）")


class BaziCalculatorTool(BaseTool):
    name: str = "八字排盘计算器"
    description: str = (
        "根据出生年月日时计算生辰八字，或使用用户提供的准确八字。"
        "如果用户提供了准确的八字，优先使用用户提供的八字。"
        "包括年柱、月柱、日柱、时柱的天干地支组合。"
        "这是八字分析的基础工具，为后续的五行分析和性格解读提供准确的数据基础。"
    )
    args_schema: Type[BaseModel] = BaziCalculatorInput

    def _run(self, name: str, birth_year: int, birth_month: int, birth_day: int, birth_hour: int,
             birth_minute: int = 0, gender: str = "", birth_place: str = "", provided_bazi: Optional[str] = None) -> str:
        """计算生辰八字"""
        try:
            # 天干地支数组
            tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

            # 五行对应
            wuxing_tg = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
                        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
            wuxing_dz = {'子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
                        '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'}

            # 如果用户提供了准确的八字，优先使用
            if provided_bazi and len(provided_bazi) == 8:
                year_zhu = provided_bazi[0:2]
                month_zhu = provided_bazi[2:4]
                day_zhu = provided_bazi[4:6]
                hour_zhu = provided_bazi[6:8]

                # 验证八字的有效性
                valid_chars = set(tiangan + dizhi)
                if all(char in valid_chars for char in provided_bazi):
                    # 处理子时跨日问题（23:00-23:59属于下一日的子时）
                    actual_birth_info = ""
                    if birth_hour == 23 and birth_minute >= 0:
                        actual_birth_info = f"（注：{birth_hour}:{birth_minute:02d}属于次日子时）"

                    result = f"""
八字排盘结果：
================
姓名：{name}
性别：{gender}
出生时间：{birth_year}年{birth_month}月{birth_day}日{birth_hour}时{birth_minute:02d}分{actual_birth_info}
出生地点：{birth_place}

八字四柱（用户提供的准确八字）：
年柱：{year_zhu} (天干{year_zhu[0]}属{wuxing_tg[year_zhu[0]]}，地支{year_zhu[1]}属{wuxing_dz[year_zhu[1]]})
月柱：{month_zhu} (天干{month_zhu[0]}属{wuxing_tg[month_zhu[0]]}，地支{month_zhu[1]}属{wuxing_dz[month_zhu[1]]})
日柱：{day_zhu} (天干{day_zhu[0]}属{wuxing_tg[day_zhu[0]]}，地支{day_zhu[1]}属{wuxing_dz[day_zhu[1]]}) → 日主
时柱：{hour_zhu} (天干{hour_zhu[0]}属{wuxing_tg[hour_zhu[0]]}，地支{hour_zhu[1]}属{wuxing_dz[hour_zhu[1]]})

五行统计：
天干：{wuxing_tg[year_zhu[0]]} {wuxing_tg[month_zhu[0]]} {wuxing_tg[day_zhu[0]]} {wuxing_tg[hour_zhu[0]]}
地支：{wuxing_dz[year_zhu[1]]} {wuxing_dz[month_zhu[1]]} {wuxing_dz[day_zhu[1]]} {wuxing_dz[hour_zhu[1]]}

注：此为用户提供的专业八字，已考虑节气、真太阳时等因素。
"""
                    return result

            # 如果没有提供八字或八字无效，则进行计算
            # 处理子时跨日问题
            calc_year = birth_year
            calc_month = birth_month
            calc_day = birth_day
            calc_hour = birth_hour

            if birth_hour == 23:  # 23:00-23:59属于下一日的子时
                calc_hour = 0  # 子时
                # 日期加一天
                birth_date = date(birth_year, birth_month, birth_day)
                next_day = date.fromordinal(birth_date.toordinal() + 1)
                calc_year = next_day.year
                calc_month = next_day.month
                calc_day = next_day.day

            # 计算年柱
            year_tg_index = (calc_year - 4) % 10
            year_dz_index = (calc_year - 4) % 12
            year_zhu = f"{tiangan[year_tg_index]}{dizhi[year_dz_index]}"

            # 计算月柱（简化算法，实际需要考虑节气）
            month_tg_index = (year_tg_index * 2 + calc_month) % 10
            month_dz_index = (calc_month + 1) % 12
            month_zhu = f"{tiangan[month_tg_index]}{dizhi[month_dz_index]}"

            # 计算日柱（使用简化的公式）
            birth_date = date(calc_year, calc_month, calc_day)
            base_date = date(1900, 1, 1)  # 基准日期
            days_diff = (birth_date - base_date).days
            day_tg_index = (days_diff + 9) % 10  # 1900年1月1日是庚子日
            day_dz_index = (days_diff + 11) % 12
            day_zhu = f"{tiangan[day_tg_index]}{dizhi[day_dz_index]}"

            # 计算时柱
            hour_dz_index = (calc_hour + 1) // 2 % 12
            hour_tg_index = (day_tg_index * 2 + hour_dz_index) % 10
            hour_zhu = f"{tiangan[hour_tg_index]}{dizhi[hour_dz_index]}"

            # 处理子时说明
            time_note = ""
            if birth_hour == 23:
                time_note = f"（注：{birth_hour}:{birth_minute:02d}属于次日子时）"

            result = f"""
八字排盘结果：
================
姓名：{name}
性别：{gender}
出生时间：{birth_year}年{birth_month}月{birth_day}日{birth_hour}时{birth_minute:02d}分{time_note}
出生地点：{birth_place}

八字四柱：
年柱：{year_zhu} (天干{tiangan[year_tg_index]}属{wuxing_tg[tiangan[year_tg_index]]}，地支{dizhi[year_dz_index]}属{wuxing_dz[dizhi[year_dz_index]]})
月柱：{month_zhu} (天干{tiangan[month_tg_index]}属{wuxing_tg[tiangan[month_tg_index]]}，地支{dizhi[month_dz_index]}属{wuxing_dz[dizhi[month_dz_index]]})
日柱：{day_zhu} (天干{tiangan[day_tg_index]}属{wuxing_tg[tiangan[day_tg_index]]}，地支{dizhi[day_dz_index]}属{wuxing_dz[dizhi[day_dz_index]]}) → 日主
时柱：{hour_zhu} (天干{tiangan[hour_tg_index]}属{wuxing_tg[tiangan[hour_tg_index]]}，地支{dizhi[hour_dz_index]}属{wuxing_dz[dizhi[hour_dz_index]]})

五行统计：
天干：{wuxing_tg[tiangan[year_tg_index]]} {wuxing_tg[tiangan[month_tg_index]]} {wuxing_tg[tiangan[day_tg_index]]} {wuxing_tg[tiangan[hour_tg_index]]}
地支：{wuxing_dz[dizhi[year_dz_index]]} {wuxing_dz[dizhi[month_dz_index]]} {wuxing_dz[dizhi[day_dz_index]]} {wuxing_dz[dizhi[hour_dz_index]]}

注：此为基础排盘结果，实际应用中需要考虑节气、真太阳时等因素。
"""
            return result

        except Exception as e:
            return f"八字计算出错：{str(e)}"


class WuxingAnalysisInput(BaseModel):
    """五行分析工具输入模式"""
    bazi_result: str = Field(..., description="八字排盘结果")


class WuxingAnalysisTool(BaseTool):
    name: str = "五行平衡分析器"
    description: str = (
        "分析八字中的五行分布情况，判断五行的强弱、缺失和过旺状态。"
        "为性格分析和运势预测提供重要的理论基础。"
    )
    args_schema: Type[BaseModel] = WuxingAnalysisInput

    def _run(self, bazi_result: str) -> str:
        """分析五行平衡"""
        try:
            # 确保输入是正确的字符串格式
            if isinstance(bazi_result, bytes):
                bazi_result = bazi_result.decode('utf-8')

            # 从八字结果中提取五行信息
            lines = bazi_result.split('\n')
            wuxing_count = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}

            # 统计五行出现次数
            for line in lines:
                for element in wuxing_count.keys():
                    wuxing_count[element] += line.count(element)

            # 分析五行平衡
            total = sum(wuxing_count.values())
            if total == 0:
                return "无法从八字结果中提取五行信息，请检查八字格式是否正确"

            analysis = "五行平衡分析：\n================\n"

            for element, count in wuxing_count.items():
                percentage = (count / total) * 100
                analysis += f"{element}：{count}个 ({percentage:.1f}%)"

                if percentage > 30:
                    analysis += " - 偏旺"
                elif percentage < 10:
                    analysis += " - 偏弱"
                else:
                    analysis += " - 平衡"
                analysis += "\n"

            # 给出建议
            analysis += "\n五行建议：\n"
            weak_elements = [e for e, c in wuxing_count.items() if c == 0]
            strong_elements = [e for e, c in wuxing_count.items() if (c / total) > 0.3]

            if weak_elements:
                analysis += f"缺失五行：{', '.join(weak_elements)}，建议在生活中适当补充。\n"
            if strong_elements:
                analysis += f"过旺五行：{', '.join(strong_elements)}，建议适当克制。\n"

            return analysis

        except Exception as e:
            return f"五行分析出错：{str(e)}"
