# Document Q&A Agent

Ask questions about any PDF using Claude's native PDF support. The full document is loaded into context — no chunking, no vector DB.

## Setup

```bash
# From the project root
pip install -r doc_qa_agent/requirements.txt

# Add your API key (if not already in .env)
cp .env.example .env   # then open .env and paste your key
```

## Run

```bash
python doc_qa_agent/agent.py path/to/your.pdf
```

### Example questions to try

- "What is the main topic of this document?"
- "Summarize the key findings in three bullet points."
- "What does section 2 say about X?"
- "Are there any tables or figures? What do they show?"
- "What are the conclusions or recommendations?"

## How it works

On the first question, the agent sends the PDF as a base64 document block alongside your question. Claude reads the entire document in a single context window — no chunking required. Every follow-up question adds only plain text; the PDF stays cached from the first turn.

The `[Cache]` line printed after each answer shows:
- `write` — tokens written to cache (first question only, ~1.25× cost)
- `read`  — tokens served from cache (all follow-ups, ~0.1× cost)
- `input` — uncached tokens (your question text)

## Context window limits

`claude-sonnet-4-5` has a 200K token context window. A typical page of text is ~500 tokens, so the model can handle PDFs up to roughly 400 pages before hitting the limit. Very large or image-heavy PDFs (scanned documents) use more tokens per page. If a document is too large, you will get an error from the API — the fix is to use a model with a larger context window or split the PDF.
