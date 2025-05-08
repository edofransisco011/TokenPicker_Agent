from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool

class TrendingToken(BaseModel):
    """ A crypto token that is in the news and attracting attention """
    name: str = Field(description="Token name")
    ticker: str = Field(description="Token ticker symbol")
    reason: str = Field(description="Reason this token is trending in the news")

class TrendingTokenList(BaseModel):
    """ List of multiple trending tokens that are in the news """
    tokens: List[TrendingToken] = Field(description="List of tokens trending in the news")

class TrendingTokenResearch(BaseModel):
    """ Detailed research on a token """
    name: str = Field(description="Token name")
    technology: str = Field(description="Technology foundations and use case")
    tokenomics: str = Field(description="Tokenomics details including supply, distribution, and utility")
    market_position: str = Field(description="Current market position and competitive analysis")
    team: str = Field(description="Team and partnership analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    risks: str = Field(description="Potential risks and concerns")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingTokenResearchList(BaseModel):
    """ A list of detailed research on all the tokens """
    research_list: List[TrendingTokenResearch] = Field(description="Comprehensive research on all trending tokens")


@CrewBase
class TokenPicker():
    """TokenPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_token_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_token_finder'],
                     tools=[SerperDevTool()])
    
    @agent
    def token_researcher(self) -> Agent:
        return Agent(config=self.agents_config['token_researcher'], 
                     tools=[SerperDevTool()])

    @agent
    def token_picker(self) -> Agent:
        return Agent(config=self.agents_config['token_picker'], 
                     tools=[PushNotificationTool()])
    
    @task
    def find_trending_tokens(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_tokens'],
            output_pydantic=TrendingTokenList,
        )

    @task
    def research_trending_tokens(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_tokens'],
            output_pydantic=TrendingTokenResearchList,
        )

    @task
    def pick_best_token(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_token'],
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the TokenPicker crew"""

        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )
            
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
        )