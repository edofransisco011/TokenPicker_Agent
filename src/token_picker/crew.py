from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List, Optional
from .tools.push_tool import PushNotificationTool

# Pydantic Models for Data Structure

# Updated for find_trending_tokens output
class TrendingToken(BaseModel):
    """ Representation of a token found to be trending based on news/narrative """
    name: str = Field(description="The token's name")
    ticker: str = Field(description="The token's ticker symbol (use 'N/A' if not easily found)")
    trending_reason: str = Field(description="Concise summary of the news/event causing the trend, based on search results")
    source_urls: List[str] = Field(description="List of actual URLs from search results supporting the reason")

class TrendingTokenList(BaseModel):
    """ List of multiple trending tokens """
    tokens: List[TrendingToken]

# Updated Pydantic model for research_trending_tokens output
class TokenResearchEntry(BaseModel):
    """ Detailed research findings for a single token """
    token_name: str = Field(description="Name of the token researched")
    news_summary: str = Field(description="Summary of recent news, updates, and narratives")
    sentiment_summary: str = Field(description="Summary of general social media/community sentiment (positive/negative/neutral)")
    website_url: Optional[str] = Field(description="URL to the token's official website")
    docs_url: Optional[str] = Field(description="URL to the token's official documentation, if found")
    repo_url: Optional[str] = Field(description="URL to the token's primary code repository, if found")
    dashboard_urls: List[str] = Field(description="List of URLs to relevant on-chain data dashboards (Dune, Etherscan, etc.)")
    tech_use_case_summary: str = Field(description="Brief summary of the token's core technology and primary use case")
    source_urls: List[str] = Field(description="List of primary source URLs used for the research summary")

class TokenResearchList(BaseModel):
    """ A list of detailed research findings for multiple tokens """
    research_list: List[TokenResearchEntry] = Field(description="Comprehensive research findings for all trending tokens")


@CrewBase
class TokenPicker():
    """TokenPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_token_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_token_finder'],
            tools=[SerperDevTool()]
        )

    @agent
    def token_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['token_researcher'],
            tools=[SerperDevTool()]
        )

    @agent
    def token_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['token_picker'],
            tools=[PushNotificationTool()]
         )

    @task
    def find_trending_tokens(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_tokens'],
            output_pydantic=TrendingTokenList, # Use updated Pydantic model
            agent=self.trending_token_finder()
        )

    @task
    def research_trending_tokens(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_tokens'],
            output_pydantic=TokenResearchList,
            context=[self.find_trending_tokens()],
            agent=self.token_researcher()
        )

    @task
    def pick_best_token(self) -> Task:
        # Note: We also updated the task description in tasks.yaml for this
        return Task(
            config=self.tasks_config['pick_best_token'],
            context=[self.research_trending_tokens()],
            agent=self.token_picker()
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
            manager_agent=manager
        )