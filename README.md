# Crypto Token Research and Selection Project

## Overview

This project demonstrates an automated system for identifying, researching, and selecting trending cryptocurrency tokens suitable for investment. Built as a showcase for portfolio purposes, it highlights practical applications of automation, data-driven decision-making, and integrated notifications.

---

## Purpose

The purpose of this project is to:

* Demonstrate automation in crypto market analysis.
* Showcase technical proficiency in Python, API integration, and agent-driven architecture.
* Serve as a practical example of skills and a conceptual illustration.

**Note:** This project is exclusively for portfolio demonstration and educational purposes.

---

## Project Structure

### Main Execution

* `main.py`:

  * Entry point of the project.
  * Initializes and executes the automated workflow.
  * Specifies inputs like crypto sector and current date for token analysis.

### Configuration

* `agents.yaml`:

  * Defines roles and goals for each automated agent, including:

    * **Crypto News Analyst:** Finds trending tokens.
    * **Senior Crypto Researcher:** Analyzes identified tokens.
    * **Token Picker:** Selects the optimal token for investment.
    * **Manager:** Coordinates tasks among agents.

* `tasks.yaml`:

  * Outlines the specific tasks each agent performs:

    * Find trending tokens.
    * Conduct detailed token research.
    * Select and notify about the best investment token.

### Agent Management

* `crew.py`:

  * Manages the creation and coordination of agents and tasks.
  * Implements structured data models for tokens and research outcomes.
  * Handles hierarchical processing through agent delegation and task execution.

### Notification System

* `push_tool.py`:

  * Implements push notifications via the Pushover API.
  * Sends real-time alerts about selected crypto tokens.
  * Handles logging, error management, and simulation for scenarios without valid credentials.

---

## How it Works

The automated workflow follows a clear sequence:

1. **Token Discovery:**

   * Searches recent crypto news to identify trending tokens within a specified sector (e.g., "meme" tokens).

2. **Token Analysis:**

   * Provides comprehensive research on each trending token, covering technology, tokenomics, market positioning, team strength, growth potential, and associated risks.

3. **Token Selection:**

   * Analyzes research outcomes to select the most promising token for investment.
   * Sends immediate notifications with investment insights.

---

## Technical Details

* **Programming Language:** Python
* **APIs Used:** SerperDev API (for data collection), Pushover API (for notifications)
* **Framework:** CrewAI for agent-driven automation
* **Data Handling:** Structured JSON reports, detailed markdown documentation

---

## Important Disclaimer

This project is designed solely as a demonstration for portfolio purposes. It should not be used for real investment decisions or relied upon for financial advice.
