# ai-agents-fluency

A hands-on learning project. Julius is building AI agents from scratch to internalize how they work. Each agent is intentionally self-contained — duplication across agents is by design and must not be refactored. The repetition IS the learning.

## Project structure

```
hello_claude.py          — bare API call, no tools
weather_agent.py         — first tool-use agent (free weather API, streaming)
web_search_agent.py      — multi-step research agent (Tavily + submit_summary pattern)
email_drafter.py         — two-tool agent with multi-turn memory and save-to-disk
doc_qa_agent/            — PDF Q&A agent using native document blocks + prompt caching
  agent.py               — main Q&A loop
  load_pdf.py            — base64 encoder utility
  setup.py               — env validation + smoke test
log.md                   — daily build notes (what was built, what broke, what was learned)
decisions/               — architectural decision records
sample_emails.json       — fixture data for email_drafter.py
summaries/               — auto-saved research outputs from web_search_agent.py
drafts/                  — auto-saved email drafts from email_drafter.py
```

## Established patterns

Every agent follows this skeleton — don't deviate without a reason:

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")   # always, for Windows

from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()
```

**Tool-use loop:** `while True` → stream → check `stop_reason` → execute tools → append `response.content` as assistant turn → append `tool_results` as user turn → repeat. Always handle `end_turn`, `tool_use`, and `max_tokens` separately.

**Streaming:** use `client.messages.stream()` with `stream.get_final_message()`. Print tokens as they arrive with `flush=True`.

**Prompt caching:** `cache_control: {"type": "ephemeral", "ttl": "1h"}` on the system prompt block and on stable tool definitions. Verify hits with `response.usage.cache_read_input_tokens`.

**Structured output via tool:** define a `submit_summary` / `draft_email` tool that Claude is instructed to call instead of responding with free text. The tool's JSON schema enforces the output shape.

**Save to disk pattern:**
- One-shot agents (web_search_agent → `summaries/`, doc_qa_agent → `qa_pairs/`): auto-save on every structured output call
- Iterative agents (email_drafter → `drafts/`): save only on explicit user `save` command, to avoid cluttering folder with intermediate drafts
- Filename convention: `YYYYMMDD_HHMMSS_slug.md`

## Python conventions

- 4-space indentation throughout — no tabs, no 2-space
- After any file edit, run the script before making more changes — Python only reports the first indentation error it hits, not all of them

## Models in use

- `claude-sonnet-4-6` — all agents

When adding new agents, default to `claude-sonnet-4-6` unless there's a reason to use something else.

## Do not

- **Do not refactor agents into a shared base class.** See `decisions/001-skip-phase1-python-refactor.md`. The agents are intentionally duplicated.
- **Do not add a `requirements.txt` to the project root.** Each subfolder (like `doc_qa_agent/`) manages its own if needed. Top-level deps are installed ad hoc.
- **Do not store API keys anywhere except `.env`.** Julius learned this the hard way on Day 2 — keys go in `.env` only, never in chat, docs, or terminal input.
- **Do not create dotfiles (`.env`, `.gitignore`) with Windows Notepad's default Save As** — it silently appends `.txt`. Use Claude Code, PowerShell `New-Item`, or set "Save as type: All Files" in Notepad before saving.

## How Julius likes to work

Build incrementally — one file at a time, explained at each step, waiting for approval before continuing. Don't write everything at once.

## Phase context

- **Phase 1 (current):** Python agents built from scratch using the Anthropic SDK directly.
- **Phase 2 (next):** n8n visual workflow builder — no Python code carries over.
- **Phase 3 (future):** Possibly LangGraph or Claude Agent SDK if multiple agents need to evolve together.
