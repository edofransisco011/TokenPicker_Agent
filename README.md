# Token Picker AI Crew

## Overview

The Token Picker AI Crew is a multi-agent system built using [CrewAI](https://crewai.com). Its purpose is to automate the process of identifying trending cryptocurrency tokens, researching them, and selecting the most promising one for potential investment based on the gathered information. The crew focuses on qualitative analysis of news, narratives, and community sentiment, and aims to locate reliable data sources for quantitative metrics.

This system is designed for users interested in discovering and getting initial insights into trending tokens within specific crypto sectors (e.g., "layer 1", "DeFi", "AI tokens").

**Disclaimer:** *This tool is for informational and educational purposes only. The output provided by this AI crew does not constitute financial advice. Always conduct your own thorough research and consult with a qualified financial advisor before making any investment decisions.*

## Core Functionality

The crew performs the following key operations:

1.  **Identifies Trending Tokens:** Scans recent web information (news, discussions) to find tokens that are currently gaining attention within a specified sector.
2.  **Researches Tokens:** For each trending token, it gathers information on recent news, social sentiment, official resources (website, docs, code repositories), and links to on-chain data dashboards.
3.  **Selects Best Token:** Analyzes the compiled research to pick the most promising token based on qualitative factors.
4.  **Notifies User:** Sends a push notification (via Pushover) with the selected token and a brief rationale.
5.  **Generates Report:** Produces a final report detailing the chosen token, the reasons for its selection, and why other researched tokens were not chosen.

## Crew Structure

The Token Picker AI Crew consists of the following agents and tasks, orchestrated in a hierarchical process managed by a `manager` agent.

---

## Agents

This section provides detailed descriptions of the AI agents used in the Token Picker Crew.

### 1. `trending_token_finder`

* **Configuration File:** `token_picker/config/agents.yaml`
* **Role:** Crypto News & Narrative Analyst for {sector}
* **Goal:** Identify tokens within the {sector} that are currently trending based on recent news, significant announcements, or high discussion volume found via web search as of {current_date}. Focus on the *narrative* or *event* causing the trend.
* **Backstory:**
    An expert crypto market analyst skilled at monitoring news feeds and online discussions. Identifies tokens gaining attention due to concrete events (partnerships, launches, major updates) or significant shifts in narrative discovered through web searches. Prioritizes providing summaries of *why* a token is trending and cites the actual web sources discovered. **MUST NOT** invent metrics, percentages, or specific dates; instead, summarizes the event/news found. Uses the current date {current_date} for context only.
* **Tools:**
    * `SerperDevTool`: For performing web searches.
* **Assigned Task:** `find_trending_tokens`

### 2. `token_researcher`

* **Configuration File:** `token_picker/config/agents.yaml`
* **Role:** Crypto Research Synthesizer for {sector}
* **Goal:** For each token provided in the context, conduct thorough web research as of {current_date} to:
    1.  Summarize recent news, announcements, and developments.
    2.  Identify and summarize prevailing community/social sentiment (positive/negative/neutral).
    3.  Find links to official project resources (website, docs, GitHub).
    4.  Find links to reliable on-chain data dashboards (e.g., Dune Analytics, Etherscan, block explorers) for metrics like wallet distribution, transaction flows.
    5.  Briefly describe the token's primary use case and technology based on research.
    Focus on synthesizing information found via web search and providing direct source URLs.
* **Backstory:**
    A meticulous research analyst specializing in the crypto space. Excels at scouring the web for the latest information on tokens, summarizing key findings, assessing sentiment, and locating primary sources and reliable data dashboards. Ensures all synthesized information is backed by cited URLs from search results. Understands the limitations of web search for precise real-time quantitative data and focuses on finding where that data lives.
* **Tools:**
    * `SerperDevTool`: For performing web searches.
* **Assigned Task:** `research_trending_tokens`

### 3. `token_picker`

* **Configuration File:** `token_picker/config/agents.yaml`
* **Role:** Quantitative Token Selection Analyst for {sector} (Note: Role name kept, but the process is now more qualitative due to data source changes).
* **Goal:**
    Evaluate the research report provided. Based *only* on the provided research summary (news, sentiment, tech/use case) and the *potential insights* suggested by the linked resources (official site, docs, repo, dashboards), select the single most promising token for potential investment. The evaluation should consider factors like: recent positive news/developments, strong positive sentiment, clear utility/use case, apparent development activity (suggested by repo link presence), and potential for insights from linked data dashboards. **Do NOT invent metrics or scores.** Base the decision on a qualitative assessment of the summarized information and the availability/implication of linked resources. After choosing, send a push notification summarizing the pick and the main reason (1 sentence).
* **Backstory:**
    A data-driven analyst with expertise in portfolio optimization and token scoring. Synthesizes data across multiple dimensions to produce a ranked list of tokens optimized for risk-reward balance. Focused on maximizing signal-to-noise in token selection. (Adapts to qualitative inputs when precise quantitative data isn't directly available from research).
* **Tools:**
    * `PushNotificationTool`: For sending notifications.
* **Assigned Task:** `pick_best_token`

### 4. `manager`

* **Configuration File:** `token_picker/config/agents.yaml`
* **Role:** Quantitative Research Project Manager for {sector}
* **Goal:** Oversee statistical and procedural rigor in token analysis across all agents as of {current_date}. Ensure consistency in output structure, data sourcing, and scoring frameworks. Monitor cumulative analysis for reliability and quality control.
* **Backstory:**
    A research lead overseeing systematic token evaluations. Focuses on maintaining reproducible pipelines and ensuring every agent performs within agreed analytical standards. Manages the hierarchical flow of tasks.
* **Tools:** None directly assigned (manages other agents).
* **Assigned Task:** Manages the overall crew process.

---

## Tasks

This section provides detailed descriptions of the tasks performed by the Token Picker Crew.

### 1. `find_trending_tokens`

* **Configuration File:** `token_picker/config/tasks.yaml`
* **Assigned Agent:** `trending_token_finder`
* **Description:**
    Identify 3-5 tokens in the {sector} that are currently trending based on recent news coverage, significant announcements, or high discussion volume discovered via web search ({current_date}).
    Focus on the *reasons* (news, events, narratives) why they are trending.
    Use the SerperDevTool to search for recent news and discussions related to tokens in the {sector}.
    Explicitly cite the source URLs for the information backing the trending reason.
    Do NOT invent metrics, percentages, specific commit numbers, or dates. Summarize the actual findings from search results.
* **Expected Output (Pydantic Model: `TrendingTokenList`):**
    A structured list (JSON format) of trending tokens. Each entry must include:
    * `name`: The token's name.
    * `ticker`: The token's ticker symbol (use 'N/A' if not easily found).
    * `trending_reason`: A concise summary (1-2 sentences) of the specific news, event, or narrative causing the token to trend, based *only* on search results.
    * `source_urls`: A list of actual URLs from the search results that support the `trending_reason`.
* **Output File:** `output/trending_tokens.json`

### 2. `research_trending_tokens`

* **Configuration File:** `token_picker/config/tasks.yaml`
* **Assigned Agent:** `token_researcher`
* **Context (Depends On):** `find_trending_tokens`
* **Description:**
    Perform in-depth web research on each trending token from the context ({current_date}). For each token:
    1.  Summarize key recent news, updates, and narratives surrounding the token using web search results.
    2.  Assess and summarize the general social media/community sentiment (positive, negative, neutral) based on search findings.
    3.  Locate and provide direct URLs to the token's official website, documentation, and primary code repository (e.g., GitHub).
    4.  Search for and provide direct URLs to relevant on-chain analytics dashboards (e.g., Dune, Etherscan, DefiLlama, specific block explorers) where metrics like wallet distribution, transaction activity, and TVL (if applicable) can be found.
    5.  Briefly summarize the token's core technology and primary use case.
    Prioritize information from reliable sources found via web search.
* **Expected Output (Pydantic Model: `TokenResearchList`):**
    A structured research report (JSON format) containing a list of objects, one for each token. Each object should include:
    * `token_name`
    * `news_summary`
    * `sentiment_summary`
    * `website_url` (Optional)
    * `docs_url` (Optional)
    * `repo_url` (Optional)
    * `dashboard_urls` (List of links)
    * `tech_use_case_summary`
    * `source_urls` (List of links)
* **Output File:** `output/research_report.json`

### 3. `pick_best_token`

* **Configuration File:** `token_picker/config/tasks.yaml`
* **Assigned Agent:** `token_picker`
* **Context (Depends On):** `research_trending_tokens`
* **Description:**
    Analyze the research report provided in the context, which includes summaries of news, sentiment, technology, use cases, and links to official resources and data dashboards for several trending tokens in the {sector}.
    Based *only* on the provided research summary (news, sentiment, tech/use case) and the *potential insights* suggested by the linked resources (official site, docs, repo, dashboards), select the single most promising token for potential investment.
    Your evaluation should consider factors like: recent positive news/developments, strong positive sentiment, clear utility/use case, apparent development activity (suggested by repo link presence), and potential for insights from linked data dashboards.
    Do NOT invent metrics or scores. Base your decision on a qualitative assessment of the summarized information and the availability/implication of linked resources.
    After choosing, send a push notification summarizing the pick and the main reason (1 sentence).
    Finally, provide a rationale explaining why the chosen token was selected and briefly why the others were not, based on the research context.
* **Expected Output:**
    A markdown report containing:
    * The name of the chosen token.
    * A detailed rationale for the selection, referencing specific points from the research context (news summary, sentiment, use case, availability of resource links).
    * A brief explanation for why other tokens from the research context were not selected.
    * Confirmation that the push notification was sent.
* **Output File:** `output/decision.md`

---

## Tools Used

* **`SerperDevTool`**: Used by `trending_token_finder` and `token_researcher` for performing web searches via serper.dev.
* **`PushNotificationTool`**: Used by `token_picker` to send notifications via Pushover. (Custom tool located in `token_picker/tools/push_tool.py`)

## Project File Structure
token_picker_project/
├── token_picker/
│   ├── init.py
│   ├── crew.py               # Defines the crew, agents, and tasks orchestration
│   ├── main.py               # Main script to run the crew
│   ├── config/
│   │   ├── agents.yaml       # Configuration for agent roles, goals, backstories
│   │   └── tasks.yaml        # Configuration for task descriptions and expected outputs
│   └── tools/
│       ├── init.py
│       └── push_tool.py      # Custom tool for sending push notifications
├── output/                   # Directory where output files (reports, JSON) are saved
│   ├── trending_tokens.json
│   ├── research_report.json
│   └── decision.md
├── README.md                 # This file
└── .env                      # For API keys and environment variables (not committed)

## Setup and Installation

1.  **Prerequisites:**
    * Python 3.10 or higher.
    * Access to a Pushover account (for notifications) and a Serper.dev API key (for web search).
    * OpenAI API key (or another compatible LLM provider key supported by CrewAI).

2.  **Clone the Repository (Example):**
    ```bash
    git clone <your-repo-url>
    cd token_picker_project
    ```

3.  **Install Dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install crewai crewai-tools pydantic python-dotenv requests
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root of the `token_picker_project` directory and add your API keys:
    ```env
    OPENAI_API_KEY="your_openai_api_key"
    SERPER_API_KEY="your_serper_api_key"
    PUSHOVER_USER="your_pushover_user_key"
    PUSHOVER_TOKEN="your_pushover_api_token"
    # Optional: specify a model
    # OPENAI_MODEL_NAME="gpt-4-turbo"
    ```

## Running the Crew

Execute the main script from the root of the project directory:

```bash
python -m token_picker.main