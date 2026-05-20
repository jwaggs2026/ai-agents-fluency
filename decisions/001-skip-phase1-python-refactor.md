# Decision: Skip Formal Refactor of Phase 1 Python Agents

## Context

After building three Python agents (`weather_agent.py`, `web_search_agent.py`, `email_drafter.py`), a natural refactor would extract the shared skeleton — env loading, Anthropic client setup, system prompt construction, tool-use loop, output formatting — into a base class or shared module. This decision record explains why that refactor was intentionally skipped.

## Decision

**Do not refactor.** Leave the three agents as independent, self-contained files.

## Reasoning

1. **The mental model already transferred.** The point of building agents from scratch three times was to internalize the pattern (env → client → prompt → tools → loop → output). Repeating it manually across three files *was* the learning. Abstracting it now would erase the repetition that made it stick.

2. **Phase 2 moves to n8n.** The next phase uses n8n (visual workflow builder), which shares no Python code with these agents. A shared Python base class has zero carry-over value into that work.

3. **No current maintenance burden.** None of the three agents are being actively modified together. The duplication isn't causing bugs or friction.

4. **Revisit condition is clear.** If Phase 3 returns to Python agents (LangGraph, Claude Agent SDK), and two or more agents need to evolve in tandem, extract the shared pattern then — when the abstraction would actually earn its keep.

## Files Affected

None. This is a no-op decision.

## Verification

No code changes to test. Marker for future-self: if you find yourself copy-pasting the tool-use loop a fourth time and both files need to stay in sync, that's the trigger to refactor.
