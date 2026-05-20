import sys
sys.stdout.reconfigure(encoding="utf-8")

import sqlite3
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "company.db"
MODEL = "claude-sonnet-4-6"

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a SQL expert assistant connected to a SQLite database called company.db.

The database contains information about a fictional company with 4 tables:
- departments: company departments with budgets
- employees: staff with titles, salaries, hire dates, and department assignments
- projects: company projects with status (active/completed/on_hold) and dates
- project_assignments: which employees are assigned to which projects and in what role

When the user asks a question:
1. Call describe_tables if you need to inspect column names or types before writing SQL.
2. Call run_sql with a valid SELECT query to fetch the answer.
3. Present the results clearly in plain English. Include the raw data when useful.

Only SELECT queries are allowed. Never attempt INSERT, UPDATE, DELETE, or DROP."""

tools = [
    {
        "name": "describe_tables",
        "description": (
            "Returns the schema for all tables in the database: column names, types, "
            "and constraints. Call this when you need to confirm column names before writing SQL."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "run_sql",
        "description": (
            "Executes a SELECT query against company.db and returns rows as JSON. "
            "Only SELECT statements are permitted."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A valid SQLite SELECT statement.",
                }
            },
            "required": ["query"],
        },
        "cache_control": {"type": "ephemeral"},  # caches both tool definitions
    },
]


def describe_tables() -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cur.fetchall()]
    schema = {}
    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        schema[table] = [
            {"column": col[1], "type": col[2], "not_null": bool(col[3]), "pk": bool(col[5])}
            for col in cur.fetchall()
        ]
    conn.close()
    return json.dumps(schema, indent=2)


def run_sql(query: str) -> str:
    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query)
        rows = [dict(row) for row in cur.fetchall()]
        conn.close()
        return json.dumps(rows, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def execute_tool(name: str, tool_input: dict) -> str:
    if name == "describe_tables":
        return describe_tables()
    if name == "run_sql":
        return run_sql(tool_input["query"])
    return json.dumps({"error": f"Unknown tool: {name}"})


def chat():
    messages = []
    print("SQL Agent ready — ask questions about company.db in plain English.")
    print("Ctrl+C to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        while True:
            with client.messages.stream(
                model=MODEL,
                max_tokens=4096,
                system=[{
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }],
                tools=tools,
                messages=messages,
            ) as stream:
                print("\nAgent: ", end="", flush=True)
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                response = stream.get_final_message()

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                print("\n")
                break
            elif response.stop_reason == "max_tokens":
                print("\n[max tokens reached]\n")
                break
            elif response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        if block.name == "run_sql":
                            print(f"\n  SQL: {block.input.get('query', '')}", flush=True)
                        else:
                            print(f"\n  → {block.name}", flush=True)
                        result = execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })
                messages.append({"role": "user", "content": tool_results})
            else:
                print(f"\n[unexpected stop_reason: {response.stop_reason}]\n")
                break


if __name__ == "__main__":
    chat()
