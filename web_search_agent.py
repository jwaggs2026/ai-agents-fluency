import os
import sys
sys.stdout.reconfigure(encoding="utf-8")

import re
from datetime import date, datetime
from dotenv import load_dotenv
from tavily import TavilyClient
import anthropic

load_dotenv()

client = anthropic.Anthropic()
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

today = date.today().strftime("%B %d, %Y")

SYSTEM_PROMPT = f"""You are a research assistant. Today's date is {today}. When answering questions:
- Always search for current information before responding
- When the user asks about recent or current events, use today's date as your reference point
- For complex questions, search multiple times: start broad, then drill into specifics, then verify key claims
- Once you have enough evidence, call submit_summary to deliver your findings — do NOT write a text response
- Every source you used must appear in the sources argument of submit_summary"""

tools = [
    {
        "name": "submit_summary",
        "description": (
            "Call this when you have finished researching and are ready to deliver your findings. "
            "This is the ONLY way to respond — do not write a text summary. "
            "Provide all four fields: topic, overview, key_findings, and sources."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "One sentence describing what was researched."
                },
                "overview": {
                    "type": "string",
                    "description": "2-3 sentences summarizing the overall findings."
                },
                "key_findings": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "3-5 bullet points of the most important findings.",
                    "minItems": 3,
                    "maxItems": 5
                },
                "sources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"}
                        },
                        "required": ["title", "url"]
                    },
                    "description": "Every source used, each with a title and URL."
                }
            },
            "required": ["topic", "overview", "key_findings", "sources"]
        }
    },
    {
        "name": "web_search",
        "description": (
            "Search the web for current information on a topic. "
            "You can and should call this tool multiple times to investigate different angles: "
            "use one search for general context, another for specific details, another for recent news or comparisons. "
            "When the user asks about recent or current events, include the current year and month in your query to ensure fresh results. "
            "Returns a list of results with title, URL, and a content snippet."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Max number of results to return (default 5).",
                    "default": 5
                }
            },
            "required": ["query"]
        },
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    }
]


def save_summary(data: dict):
    os.makedirs("summaries", exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", data["topic"].lower()).strip("-")[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"summaries/{timestamp}_{slug}.md"

    lines = [
        f"# {data['topic']}",
        f"\n**Date:** {date.today().strftime('%B %d, %Y')}",
        "\n## Overview",
        data["overview"],
        "\n## Key Findings",
        *[f"- {f}" for f in data["key_findings"]],
        "\n## Sources",
        *[f"{i}. [{s['title']}]({s['url']})" for i, s in enumerate(data["sources"], 1)],
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[Agent] Summary saved to {filename}")


def format_summary(data: dict):
    print("\n" + "=" * 60)
    print(f"TOPIC: {data['topic']}")
    print("=" * 60)
    print(f"\nOVERVIEW\n{data['overview']}")
    print("\nKEY FINDINGS")
    for finding in data["key_findings"]:
        print(f"  • {finding}")
    print("\nSOURCES")
    for i, source in enumerate(data["sources"], 1):
        print(f"  {i}. {source['title']}")
        print(f"     {source['url']}")
    print("=" * 60 + "\n")


def web_search(query: str, max_results: int = 5) -> str:
    print(f"  [Tool] Searching: '{query}' (max {max_results} results)...")
    response = tavily.search(query=query, max_results=max_results)

    results = []
    for r in response.get("results", []):
        results.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content']}"
        )

    if not results:
        return "No results found."

    return "\n\n---\n\n".join(results)


def run_agent(user_message: str, messages: list = None):
    if messages is None:
        messages = []

    print(f"\n[User] {user_message}")
    print("-" * 50)

    messages.append({"role": "user", "content": user_message})

    while True:
        summary_submitted = False
        print("\n[Agent] Sending request to Claude...")

        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            tools=tools,
            messages=messages
        ) as stream:
            printed_header = False
            for text in stream.text_stream:
                if not printed_header:
                    print("\n[Claude] ", end="", flush=True)
                    printed_header = True
                print(text, end="", flush=True)
            response = stream.get_final_message()

        u = response.usage
        print(f"\n[Agent] Stop reason: {response.stop_reason}")
        print(f"[Cache] write={u.cache_creation_input_tokens} read={u.cache_read_input_tokens} input={u.input_tokens}")

        if response.stop_reason == "end_turn":
            print()
            return

        if response.stop_reason == "max_tokens":
            print("\n[Agent] Warning: response was cut off (max_tokens reached). Consider raising max_tokens.\n")
            return

        if response.stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            tool_results = []
            for tool_use_block in tool_use_blocks:
                tool_name   = tool_use_block.name
                tool_input  = tool_use_block.input
                tool_use_id = tool_use_block.id

                print(f"\n[Agent] Claude requested tool: '{tool_name}'")
                print(f"[Agent] Tool input: {tool_input}")

                if tool_name == "submit_summary":
                    format_summary(tool_input)
                    save_summary(tool_input)
                    result = "Summary submitted successfully."
                    summary_submitted = True
                elif tool_name == "web_search":
                    result = web_search(
                        tool_input["query"],
                        tool_input.get("max_results", 5)
                    )
                    print(f"[Agent] Tool result preview: {result[:120]}...")
                else:
                    result = f"Unknown tool: {tool_name}"

                print("-" * 50)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": result
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            if summary_submitted:
                return


if __name__ == "__main__":
    print("Web Search Agent — type 'quit' to exit\n")
    messages = []

    while True:
        topic = input("Enter a topic to research: ").strip()
        if topic.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break
        run_agent(topic, messages)
