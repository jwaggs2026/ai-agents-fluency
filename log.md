---

## 2026-05-16 (Sat) — Week 3 Weekly Review

**n8n:** Easiest of the three. The visual canvas makes it natural to map a workflow before building it. Claude Code scaffolded the Local Vendor Research Agent quickly and got the architecture right on the first pass. The harder part was the back end — prompts, node expressions, and data passing all needed manual debugging after the initial build. The pattern: Claude Code gets you 70%, you fix the rest.

**crewAI:** Similar visual structure to n8n; the AI assistant did most of the heavy lifting. Main friction was token usage — significantly more than n8n for equivalent tasks. Less familiar with it so the learning curve felt steeper, but high potential with more time.

**LangGraph:** Most code-heavy of the three. DeepLearning.AI courses made the concepts clear but implementation is verbose. The SQL agent was written by Claude via the Anthropic SDK rather than built independently — a legitimate workflow, but LangGraph fluency isn't there yet.

**VS Code + Claude Code:** Meaningfully better than PowerShell. More readable, easier to debug, and the context Claude Code maintains makes multi-step builds more manageable. Worth continuing here.

**Phase 3 signal:** n8n is the most natural. LangGraph has the most control. The open question: go deeper on ease (n8n + more complex workflows) or deeper on code (LangGraph + real programmatic agents)?

---

## 2026-05-16 (Sat) — Phase 2 Day 9

**Setup:** Installed VS Code with the Claude Code extension.

**Built:** Vendor Research Agent in n8n via Claude Code.

- Claude Code mapped out the entire agent architecture quickly
- Had issues with sub-agents and Tavily integration inside the agent
- Spent time manually fixing prompts and other system items to refine the output toward the expected result

**Cost:** $0.27 | **Hours:** ~8

---

## 2026-05-15 (Fri) — Phase 2 Day 8

**Finished:** Lead-Research Agent in CrewAI (1 hr carryover from Day 7).

**CrewAI vs. n8n comparison:**
- CrewAI node implementation was harder, cost more ($2.90), and didn't work well with Tavily
- n8n (no-code) was easier and handled more of the troubleshooting automatically
- Same agent, different frameworks — clear winner: n8n for this use case

**Learning:** Completed "AI Agents in LangGraph" course on DeepLearning.AI.

**Built:** SQL agent (Anthropic SDK) — natural language → SQLite queries against a local `company.db`. Claude Code wrote all the code.

- Two tools: `describe_tables` (schema inspection) and `run_sql` (SELECT execution)
- Prompt caching on system prompt and tool definitions
- Same tool-use loop pattern as Phase 1 agents

**Bugs caught and fixed:**
- Debug 1: Typing Python directly into PowerShell instead of running `sql-agent.py` — fixed by cd-ing into the correct subfolder
- Debug 2: `.env` not loading — fixed by matching the format from the original Ai-Agents-Fluency folder `.env`

**Notes:**
- LangGraph course was heavy on code — Claude chat and ChatGPT helped with getting started (no template to follow)
- Harder to get started on a new framework without an existing pattern to follow

**Costs:** CrewAI: $2.90 | SQL agent: $0.08

**Hours:** ~8

---

## 2026-05-14 (Thu) — Phase 2 Day 7

**Built:** Lead-Research Agent rebuilt in CrewAI — direct comparison to n8n build underway.

- Completed "Multi AI Agent Systems with CrewAI" course on DeepLearning.AI
- Carried ~1 hour of build work into Thursday to finish the CrewAI version of the Lead-Research Agent
- Side-by-side comparison with n8n version in progress — same agent, different framework

**Hours:** ~7

---

## 2026-05-12–13 (Tue–Wed) — Phase 2 Days 5–6

**Built:** Two agents.

**Content Repurposing Agent**
- Planned on paper first
- Added Google Sheets node first, then added an IF node to fix recursive trigger loops and stale row processing
- **Learning input:** 2 YouTube videos + 1 Skool course
- **Cost:** $0.48

**Email Support Triage Agent**
- Planned on paper first
- Removed the email label workflow — going to separate agents instead
- **Learning input:** 1 YouTube video + 1 Skool course
- **Cost:** $0.07

**Observations:**
- Mapping before building is paying off — workflows becoming easier
- Agent workflows still need work; regular node workflows are more intuitive right now

**Hours:** ~9 (across both days)

---

## 2026-05-11 (Mon) — Phase 2 Day 4

**Learning input:** Started "AI Agentic Design Patterns with AutoGen" course on DeepLearning.AI. Watched 2 YouTube videos on content repurposing agents.

**Built:** Content repurposing agent — mapped on paper, started building in n8n.

**Hours:** ~4

---

## 2026-05-10 (Sun) — Phase 2 Day 3

**Built:** Lead-Research Agent — planned on paper first, then built in n8n.

- 8-node pipeline: submission form → validation → research → scoring → CRM data formatting → Google Sheet → switch → lead alert email
- Added a 4th lead alert tier: *needs enrichment* (for leads with thin internet presence)
- 8 workflow notes added flagging future improvements
- **Known issue:** Hard to find cold leads for small businesses with thin internet presence — scoring output may need calibration before use in any real or client context
- **Learning input:** 2 YouTube videos on n8n lead agents

**Decisions / Notes:**
- Phase 3 direction gut-check: leaning toward deepening n8n node fluency before moving to code frameworks — the mapping mindset (data flowing node to node) is clicking in a way Python didn't make tangible
- "Plan on paper first" habit is paying off — agent architecture pattern becoming intuitive
- Do not use Lead-Research Agent in real or client work until scoring output is reviewed and validated

**Costs:** Claude API remaining $18.23 of $50 starting budget (~$31.77 spent to date). API spend accelerating in Phase 2 — monitor closely; consider caching or batching where possible.

**Hours:** ~9

---

## 2026-05-09 (Sat) — Phase 2 Day 2

**Built:** Two n8n agents from templates.

- **Meeting Notes → Action Items:** Cloned template. Removed output parser node — moved parsing logic directly into the AI agent prompt. Swapped template LLM for Claude.
- **Contact Enrichment:** Cloned template. Removed the IF function input node. Swapped search tool for Tavily, LLM for Claude. Added 2 workflow notes flagging future improvements.

**Resolved:** Google Sheets OAuth — deferred from Day 1, closed during Contact Enrichment build.

**Decisions / Notes:**
- Tavily already in stack — natural swap over SerpAPI/ScrapingBee
- Keeping output parsing in the agent rather than a separate node feels cleaner; watch whether this causes issues at scale

**Costs:** Claude API $8.74 (Phase 2 running total: ~$8.74). n8n $24/mo subscription started.

**Hours:** ~8.5

---

## 2026-05-08 (Fri) — Phase 2 Day 1

**Built:** First n8n AI agent — email assistant. Pattern: trigger → AI Agent node → tools → output.

**Learning input:** 5 Nate Herk videos + 2 Cole Medin videos. Build-along format worked well — passive watching then active replication.

**Issue:** Google Sheets credential won't connect (likely OAuth flow issue). Deferred to weekend — not a blocker but a real gap to close before Phase 2 Day 4–5 builds.

**Transfer learning observations:** n8n's AI Agent node maps cleanly to Phase 1's Python tool-use loop. System prompt goes in agent config. Tools are sub-nodes attached to the agent. The mental model transferred fully — no relearning, just visual translation.

**Hours:** ~8

**Next (Sat/Sun):** Fix Google Sheets OAuth. Build Lead-Research Agent (originally planned for Phase 2 Day 3).

---

## ✅ PHASE 1 COMPLETE — May 6, 2026

**Four foundational Python agents built:**
- `weather_agent.py` — first tool-use agent, streaming, free weather API
- `web_search_agent.py` — multi-step research agent, Tavily, structured output via tool
- `email_drafter.py` — two-tool agent, multi-turn conversation, save-to-disk
- `doc_qa_agent/agent.py` — native document blocks, prompt caching, Q&A save

**Patterns internalized:**
- Tool-use loop (`while True` → stream → stop_reason → execute → append → repeat)
- Structured output via tool (JSON schema as output contract, not prose instructions)
- Multi-turn conversation (preserving `messages` list across iterations)
- Multi-tool selection (tool descriptions drive Claude's decisions, not code logic)
- Prompt caching (`cache_control` + verifying with `cache_read_input_tokens`)
- Native document blocks (base64 PDF in first message, cached for follow-ups)

**Skipped:** Formal refactor of agents into shared base class — see `decisions/001-skip-phase1-python-refactor.md`

**Total Phase 1 time:** ~25 hours (rough estimate)

**Phase 1 API spend:** $20.09 total across 4 agents over ~6 days (~$3.35/day average). Heaviest single agent: `doc_qa_agent` (prompt caching + large PDFs = high token volume on first load).

**Phase 2 cost calibration:** Budget $2–5/day — n8n cloud handles most API routing; Claude API calls are occasional rather than every interaction.

**Taking forward:**
- Agent design starts with tool description writing — Claude reads descriptions to decide when and how to use tools; the description is the interface
- LLMs only know what's in context — current date, user identity, domain rules all have to be injected explicitly
- User identity belongs in the system prompt — prevents placeholder hallucination (`[Your Name]`, etc.)

**Still fuzzy on:** Agent loop edge cases (limited failure mode catalog so far); tool description writing from scratch (still relying on Claude Code to draft them). Plan: deliberate practice in week 2.

**Next: Phase 2 — n8n visual workflow building.** Different platform, same agent concepts.

---

## 2026-05-07 (Thu) — Day 8 — Phase 1 → Phase 2 Transition

**Phase 1 wrap:**

- API spend audit complete: $20.09 across 6 days (~$3.35/day average)
- All four agents working, portfolio folders populated
- CLAUDE.md verified accurate
- Phase 1 officially closed

**Phase 2 setup:**

- n8n cloud account active
- Skool: AI Automation Society (free tier) — re-evaluate Plus at end of Phase 2 only if going agency direction
- YouTube: Nate Herk + Cole Medin subscribed; 5 others deferred until Phase 3+ when actually needed
- X follows: 8 builders, notifications muted
- Watched Nate Herk's first n8n agent video (passive viewing) — saw the AI Agent node, system prompt configuration, tool wiring; direct mapping to Python patterns from Phase 1

**Skipped (intentionally):** Anthropic Academy cert, portfolio audit, ADR. Cert fits in week 2 low-energy slot. Portfolio is sufficient for now.

**Hours:** ~6

**Next (Friday May 8):** Phase 2 Day 1, 8–9 hours, n8n setup + first agent.

---

## 2026-05-06 (Wed) — Day 7

**Built:** `doc_qa_agent/agent.py` — fourth foundational agent. Loads a PDF via native document blocks, caches it with a 1-hour TTL, and runs a multi-turn Q&A loop. Added `save` command to write Q&A pairs to `qa_pairs/YYYYMMDD_HHMMSS_slug.md`.

- **Native document blocks:** PDF base64-encoded by `load_pdf.py`, sent as `{"type": "document", "source": {"type": "base64", ...}}` in the first message only — subsequent turns are plain text, PDF stays cached
- **Prompt caching verified:** 12,442 tokens cached on first question; follow-up questions read from cache at ~10% of original cost (~90% savings)
- **Save feature:** `save` command (same pattern as `email_drafter.py`) writes the most recent Q&A pair to `qa_pairs/` — no auto-save, only on explicit command

**Bugs caught and fixed:**
- Indentation error in `agent.py` — `response = client.messages.create(` was left at column 0 after a debug-print block was removed; Python crashed on the next indented line rather than the broken one
- Stray `.env.txt` — Windows Notepad silently appended `.txt` when saving the `.env` file; fixed with `Rename-Item`; added Notepad caveat to `CLAUDE.md`

**Key concepts internalized:**
- Debug prints can silently break indentation on removal — always run the script after any edit before continuing
- `cache_write` tokens on first question, `cache_read` on every follow-up — the cache line in output is the fastest way to confirm it's working
- Python stops at the first indentation error it finds; subsequent errors only surface after the first is fixed

**Hours:** ~4

---

## 2026-05-05 (Tue) — Day 6

**Built:** `email_drafter.py` — a multi-tool email drafting agent with conversation memory and save-to-disk.

- **Two-tool agent:** `lookup_recent_emails` searches `sample_emails.json` (filter by sender/thread/keyword, ranked by relevance) and `draft_email` delivers structured output — same forced-tool pattern as `web_search_agent.py` but with `tool_choice: auto` so Claude decides which to call first
- **Persistent user identity:** `USER_PROFILE` dict injected into system prompt at startup — Claude always signs as Daniel, never uses `[Your Name]` placeholders
- **Multi-turn conversation loop:** `messages` list lives in `__main__` and is passed into each `run_agent()` call, so Claude retains full context across iterations ("make it shorter", "add a P.S.")
- **Explicit save command:** typing `save` writes the last draft to `drafts/YYYYMMDD_HHMMSS_recipient_subject.md` — no auto-saving on every draft, only on user intent; cleared after save so double-saving is blocked
- **Lenient search logic:** sender filter always returns results; search_query ranks rather than filters when a sender is already specified; word-by-word matching so "missing data filter" finds an email about "reporting"

**Bugs caught and fixed:**

- `[Your Name]` in signatures — system prompt didn't include identity; fixed by adding `USER_PROFILE` injected as an f-string before any behavioral instructions
- Lookup AND-logic too strict — `sender` + `search_query` both had to match, so "Jenny + missing data filter" returned empty because her email talks about "reporting"; fixed by making sender a hard filter and search_query a ranking signal only
- Over-eager lookup — Claude called `lookup_recent_emails` for a dentist thank-you email; fixed by adding explicit DO NOT examples to the tool description (`dentists, doctors, family, friends`, `cold outreach`)
- Duplicate saves — typing `save` twice wrote two identical files; fixed by setting `last_draft = None` immediately after a successful save

**Key concepts internalized:**

- Multi-tool agents need careful tool descriptions — Claude reads them to decide when to use which tool; DO/DON'T examples with concrete nouns work better than abstract rules
- Tool functions should fail loose: return what you have, don't require all filters to match
- User identity belongs in the system prompt, not re-stated in every user message
- Multi-turn conversation = preserving the `messages` list across loop iterations; Claude's context is the list, not magic
- Don't ask the LLM to decide things it can't know — explicit user commands (`save`) beat `final_version: bool` parameters Claude would guess wrong
- Caching tradeoff: cached prefix saves tokens on long sessions; single-shot calls don't benefit until the second turn

**Still fuzzy on:** Agent loops at the edges — the happy path is clear but I don't yet have intuition for failure modes (what happens if Claude calls both tools at once, or loops unexpectedly). Tool description writing — I can follow the pattern but still rely on Claude Code to draft descriptions from scratch.

**Skipped:** Formal refactor of the 3 agents into a shared base pattern. The common structure (load env → client → system prompt → tools → tool-use loop → print output) is visible, but the mental refactor already happened during the builds — that repetition was the point. Phase 2 moves to n8n which doesn't share Python code anyway. Will revisit if Phase 3 returns to Python agents (LangGraph or Claude Agent SDK) and two agents need to evolve in tandem. See `decisions/001-skip-phase1-python-refactor.md` for full reasoning.

**Hours:** ~4

---

## 2026-05-01 (Fri) — Day 5

**Built:** `web_search_agent.py` — a full web-search summarizer agent using Tavily and Claude.

- Tavily integration with the `web_search` tool returning title/URL/snippet blocks
- Parallel tool calls — Claude fires multiple searches per roundtrip automatically
- Multi-step search reasoning — Claude searches 6–10 times across 3–5 API roundtrips before answering
- Structured output via the `submit_summary` tool pattern — Claude calls a "fake" tool to deliver findings instead of writing free-form text; format is enforced in Python, not by Claude's discretion
- Date-awareness fix — `date.today()` injected into system prompt at runtime so Claude knows today is May 1, 2026 and anchors search queries to the right year/month
- Prompt caching with 1-hour TTL — `cache_control` on the system prompt block and the last tool in the array; verified with `cache_creation_input_tokens` / `cache_read_input_tokens` from `response.usage`; saw cross-run reads of 3,000–8,000 tokens
- `save_summary()` — every `submit_summary` call writes a `summaries/YYYYMMDD_HHMMSS_topic-slug.md` file automatically; 7 portfolio summaries saved today

**Broke:** Two bugs caught and fixed mid-session:
- `max_tokens=2048` was too low for long comparison answers — Claude's response was cut off and the loop silently restarted from scratch. Fixed by raising to 4096 and adding an explicit `max_tokens` guard to the loop.
- `{"type": "ephemeral", "ttl": 3600}` rejected by the API — the TTL value must be the string `"1h"`, not an integer.

**Learned:**

- Claude doesn't know the current date unless you tell it — biggest lesson of the day. Without `today` in the system prompt, every "latest news" query returned results from 2025.
- Structured output is achieved by defining a tool Claude is instructed to call — not by formatting instructions. The tool's JSON schema enforces the shape; the schema is the contract, not the prose.
- Tool descriptions are real prompt engineering. Claude reads them to decide when to call a tool and what to expect back. The three-sentence pattern (what it does / when to use it / what it returns) directly shapes Claude's behavior.
- Prompt caching is two `cache_control` markers plus verifying with usage metrics. The 5-minute TTL is too short for this agent's query cadence — 1-hour TTL is the right default for conversational agents.
- `stop_reason` values matter: `end_turn`, `tool_use`, and `max_tokens` each need their own handler. A missing `max_tokens` branch causes silent infinite retries.

**Still fuzzy on:** Agent loops in general — the while-True structure makes sense when I trace through it, but I don't yet have the intuition for when the loop will misbehave. General coding — still relying heavily on Claude Code to write the Python; need to spend more time reading and modifying code myself.

**Next:** Study the agent loop more carefully. Try modifying `web_search_agent.py` by hand — change a tool description, add a parameter, break something intentionally and fix it.

**Hours:** ~5

---

## 2026-04-29 (Wed) — Day 4

**Built:** First tool-using agent (`weather_agent.py`). Implemented the full tool-use loop, tested with 20+ different prompts, added streaming output, and fixed geolocation for smaller towns like Salisbury, NC and Cleveland, NC.

**Broke:** Nothing major — geolocation for small towns needed fixing, which Claude Code helped resolve.

**Learned:** Claude Code did the agent building and explained the info and process at each step. Understanding the code and following prompt inputs will take time. Claude Code made it easy to edit and fix the weather agent. Need to keep spending time on understanding the code and the coding process.

**Next:** Keep working on understanding the code — trace through the tool-use loop and study what each part does before moving to more complex agents.

**Hours:** 4

---

## 2026-04-27 (Mon) — Day 2

**Built:** Python 3.14, Anthropic SDK, `.env`, `.gitignore`. Got `hello_claude.py` running — first real API call with Claude's response coming back.

**Broke:** Pasted a live API key into chat on claude.ai, then again directly into Claude Code's terminal. Rotated keys twice. Also moved project off OneDrive to `C:\Users\juliu\Projects\Ai-Agents-Fluency` to keep credentials out of cloud sync.

**Learned:** API keys belong only in `.env` files and a password manager — never in any chat, doc, or terminal input. Reviewed Anthropic prompt engineering docs: clarity, examples, XML tags for structure.

**Next:** Actual learning content — Karpathy LLM video + Building Effective Agents essay.

**Hours:** ~7.5 (most of it Windows setup + security cleanup, less than expected on actual learning)

---

## 2026-04-25 (Sat) — Day 0

**Built:** Project folder, Git for Windows, Node.js v24.15.0, Claude Code via npm. Authenticated with Claude Pro sub.

**Broke:** Native Claude Code installer half-failed (missing Git). Switched to npm install. PowerShell execution policy needed updating to RemoteSigned.

**Learned:** Windows dev setup is fiddly but the error chain is normal first-time stuff.

**Next:** Sign up for Anthropic API console, load $40 credit, generate API key. Tomorrow: Karpathy LLM video + Building Effective Agents essay.

**Hours:** 4
