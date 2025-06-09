from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AgentProject():
    """八字分析智能体团队"""
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # 使用DeepSeek API（修复配置）
    deepseek_llm = LLM(
        model="deepseek/deepseek-chat",
        api_key=os.getenv("DEEP_SEEK_KEY"),
        base_url=os.getenv("DEEP_SEEK_URL"),
        temperature=0.7,
        max_tokens=4000
    )

    # 八字分析智能体定义（移除工具调用，直接使用专业知识）
    @agent
    def bazi_calculator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['bazi_calculator'],
            verbose=True,
            llm=self.deepseek_llm
        )

    @agent
    def wuxing_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['wuxing_analyzer'],
            verbose=True,
            llm=self.deepseek_llm
        )

    @agent
    def personality_interpreter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['personality_interpreter'],
            verbose=True,
            llm=self.deepseek_llm
        )

    @agent
    def fortune_predictor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['fortune_predictor'],
            verbose=True,
            llm=self.deepseek_llm
        )

    @agent
    def life_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['life_advisor'],
            verbose=True,
            llm=self.deepseek_llm
        )

    # 八字分析任务定义
    @task
    def calculate_bazi_task(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_bazi'],
            agent=self.bazi_calculator_agent(),
        )

    @task
    def analyze_wuxing_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_wuxing'],
            agent=self.wuxing_analyzer_agent(),
            context=[self.calculate_bazi_task()]
        )

    @task
    def interpret_personality_task(self) -> Task:
        return Task(
            config=self.tasks_config['interpret_personality'],
            agent=self.personality_interpreter_agent(),
            context=[self.calculate_bazi_task(), self.analyze_wuxing_task()]
        )

    @task
    def predict_fortune_task(self) -> Task:
        return Task(
            config=self.tasks_config['predict_fortune'],
            agent=self.fortune_predictor_agent(),
            context=[self.calculate_bazi_task(), self.analyze_wuxing_task(), self.interpret_personality_task()]
        )

    @task
    def provide_life_guidance_task(self) -> Task:
        return Task(
            config=self.tasks_config['provide_life_guidance'],
            agent=self.life_advisor_agent(),
            context=[self.calculate_bazi_task(), self.analyze_wuxing_task(),
                    self.interpret_personality_task(), self.predict_fortune_task()]
        )

    @crew
    def crew(self) -> Crew:
        """创建八字分析智能体团队"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        return Crew(
            agents=[
                self.bazi_calculator_agent(),
                self.wuxing_analyzer_agent(),
                self.personality_interpreter_agent(),
                self.fortune_predictor_agent(),
                self.life_advisor_agent(),
            ], # 八字分析智能体列表
            tasks=[
                self.calculate_bazi_task(),
                self.analyze_wuxing_task(),
                self.interpret_personality_task(),
                self.predict_fortune_task(),
                self.provide_life_guidance_task(),
            ], # 八字分析任务列表
            process=Process.sequential,
            planning=True,
            planning_llm=self.deepseek_llm,
            verbose=True,

        )
