# Email Drafter

A conversational CLI agent that drafts emails on your behalf using Claude. It can look up recent emails from local sample data to provide context when replying or following up, then produces a complete draft with subject line, body, and tone.

## How it works

1. You describe what you want to write — who it's for, the purpose, and your desired tone.
2. The agent decides whether to look up relevant past emails for context (`lookup_recent_emails`).
3. It drafts a complete email and displays it (`draft_email`).
4. Type `save` to persist the draft as a Markdown file in the `drafts/` folder.

## Setup

1. Install dependencies:
   ```
   pip install anthropic python-dotenv
   ```
2. Add your Anthropic API key to a `.env` file:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
3. Populate `sample_emails.json` with at least 8 work emails (used for context lookups).

## Running

```
python email_drafter.py
```

**Commands at the prompt:**
- Type any email request to generate a draft.
- `save` — save the last draft to `drafts/`.
- `quit` / `exit` / `q` — exit the program.
