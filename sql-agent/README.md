# SQL Agent

A conversational AI agent that answers natural-language questions about a SQLite database using Claude and tool use.

## What it does

The agent connects to `company.db` — a fictional company database — and lets you query it in plain English. Claude decides when to inspect the schema (`describe_tables`) and when to run a query (`run_sql`), then summarizes the results conversationally.

Only `SELECT` queries are permitted; the agent will refuse any attempt to mutate data.

## Database schema

`company.db` contains four tables:

| Table | Description |
|---|---|
| `departments` | Departments with budgets |
| `employees` | Staff with titles, salaries, hire dates, and department |
| `projects` | Projects with status (`active` / `completed` / `on_hold`) and dates |
| `project_assignments` | Employee-to-project assignments with roles |

## Setup

```bash
pip install anthropic python-dotenv
```

Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-...
```

Seed the database (only needed once):

```bash
python seed.py
```

## Usage

```bash
python sql-agent.py
```

Then ask questions in plain English:

```
You: Which department has the highest budget?
You: List all active projects and the employees assigned to them.
You: What is the average salary in Engineering?
```

Press `Ctrl+C` to exit.

## How it works

- Uses the Anthropic Python SDK with streaming and prompt caching
- Two tools exposed to Claude: `describe_tables` and `run_sql`
- The system prompt and tool definitions are cached with `cache_control: ephemeral` to reduce latency on follow-up turns
- Maintains full conversation history so Claude can answer follow-up questions in context
