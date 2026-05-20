import os
import sys
sys.stdout.reconfigure(encoding="utf-8")

from datetime import date, datetime
from dotenv import load_dotenv
import anthropic
import json
import re

load_dotenv()

client = anthropic.Anthropic()

today = date.today().strftime("%B %d, %Y")

USER_PROFILE = {
    "name": "Daniel Waggoner",
    "title": "Founder",
    "company": "AI Consulting (placeholder)",
    "email": "juliuswaggoner@gmail.com",
    "default_signature_style": "first name only"
}

SYSTEM_PROMPT = f"""You are an email drafting assistant. Today's date is {today}.

You are drafting emails on behalf of {USER_PROFILE['name']}, who is {USER_PROFILE['title']} at {USER_PROFILE['company']}. When signing emails, use '{USER_PROFILE['name'].split()[0]}' (first name only) unless the user specifies otherwise. Never use placeholder text like [Your Name] — always use the real values from the user profile. If a field is missing, omit it entirely rather than inserting a placeholder.

Your job is to write clear, well-structured emails on behalf of the user. When given a request:
- Identify the recipient, purpose, and desired tone from the user's message
- Draft a complete email with a subject line and body
- Always call draft_email — do not write a text response

Match the tone exactly: formal emails are polished and professional, casual emails are relaxed and natural, friendly emails are warm but still clear."""

tools = [
    {
        "name": "lookup_recent_emails",
        "description": (
            "Search the user's recent work emails stored locally. "
            "USE this tool when: the user references a known work contact by name, "
            "asks to reply or follow up on a work email, mentions a coworker, client, or vendor "
            "they have previously corresponded with, or references a past conversation or thread. "
            "DO NOT use this tool for: personal correspondence (dentists, doctors, family, friends), "
            "cold outreach to contacts the user has never emailed before, "
            "or when the user provides all the context needed inline. "
            "When in doubt, skip the lookup and draft directly — the user can ask for a revision if needed."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "Keyword to match against subject and body (case-insensitive). Optional."
                },
                "sender": {
                    "type": "string",
                    "description": "Filter by sender name or email address (partial match). Optional."
                },
                "thread_id": {
                    "type": "string",
                    "description": "Return only emails in this thread. Optional."
                },
                "limit": {
                    "type": "integer",
                    "description": "Max number of emails to return. Defaults to 5.",
                    "default": 5
                }
            },
            "required": []
        },
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    },
    {
        "name": "draft_email",
        "description": (
            "Call this to deliver a drafted email. This is the ONLY way to respond — "
            "do not write a text reply. Fill in all required fields based on the user's request."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "recipient_name": {
                    "type": "string",
                    "description": "First name (or full name) of the person the email is addressed to."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line."
                },
                "body": {
                    "type": "string",
                    "description": "Full email body, including greeting and sign-off."
                },
                "tone": {
                    "type": "string",
                    "enum": ["formal", "casual", "friendly", "professional"],
                    "description": "The tone used when drafting this email."
                },
                "purpose": {
                    "type": "string",
                    "description": "One sentence describing what this email achieves (e.g. 'Reschedules Tuesday meeting to later in the week')."
                }
            },
            "required": ["recipient_name", "subject", "body", "tone"]
        },
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    }
]


def format_draft(data: dict):
    purpose = data.get("purpose", "")

    print("\n" + "=" * 60)
    print("DRAFTED EMAIL")
    print("=" * 60)
    if purpose:
        print(f"Purpose : {purpose}")
    print(f"To      : {data['recipient_name']}")
    print(f"Tone    : {data['tone']}")
    print(f"Subject : {data['subject']}")
    print("-" * 60)
    print(data["body"])
    print("=" * 60 + "\n")


def save_draft(data: dict):
    os.makedirs("drafts", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recipient_slug = re.sub(r"[^a-z0-9]+", "_", data["recipient_name"].lower()).strip("_")
    subject_slug = re.sub(r"[^a-z0-9]+", "-", data["subject"].lower()).strip("-")[:40]
    filename = f"drafts/{timestamp}_{recipient_slug}_{subject_slug}.md"

    purpose = data.get("purpose", "")
    lines = []
    if purpose:
        lines.append(f"**Purpose:** {purpose}\n")
    lines += [
        f"**From:** {USER_PROFILE['name']} <{USER_PROFILE['email']}>",
        f"**To:** {data['recipient_name']}",
        f"**Subject:** {data['subject']}",
        f"**Tone:** {data['tone']}",
        "",
        "---",
        "",
        data["body"],
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[Saved] {filename}")


def lookup_recent_emails(
    search_query: str = None,
    sender: str = None,
    thread_id: str = None,
    limit: int = 5
) -> str:
    print(f"  [Tool] Looking up emails — query={search_query!r} sender={sender!r} thread={thread_id!r} limit={limit}")

    with open("sample_emails.json", encoding="utf-8") as f:
        emails = json.load(f)

    if sender:
        sender_words = sender.lower().split()
        emails = [e for e in emails if all(w in e["from"].lower() for w in sender_words)]
    if thread_id:
        emails = [e for e in emails if e["thread_id"] == thread_id]

    if search_query:
        words = search_query.lower().split()

        def score(email):
            fields = " ".join([email["subject"], email["body"], email["from"]]).lower()
            return sum(1 for w in words if w in fields)

        if sender or thread_id:
            emails = sorted(emails, key=score, reverse=True)
        else:
            emails = sorted([e for e in emails if score(e) > 0], key=score, reverse=True)

    emails = emails[:limit]

    if not emails:
        return json.dumps({"results": [], "message": "No matching emails found."})

    results = []
    for e in emails:
        results.append({
            "id": e["id"],
            "from": e["from"],
            "to": e["to"],
            "subject": e["subject"],
            "date": e["date"],
            "thread_id": e["thread_id"],
            "snippet": e["body"][:200].replace("\n", " ") + ("..." if len(e["body"]) > 200 else "")
        })

    return json.dumps({"results": results})


def run_agent(user_message: str, messages: list):
    messages.append({"role": "user", "content": user_message})
    last_draft = None

    while True:
        print("\n[Agent] Sending request to Claude...")

        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            tools=tools,
            tool_choice={"type": "auto"},
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
        print(f"\n[Cache] write={u.cache_creation_input_tokens} read={u.cache_read_input_tokens} input={u.input_tokens}")
        print(f"[Agent] Stop reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            print("[Agent] Warning: Claude responded with text instead of calling draft_email.")
            return last_draft

        if response.stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            tool_results = []

            for block in tool_use_blocks:
                print(f"\n[Agent] Tool called: '{block.name}'")
                print(f"[Agent] Input: {block.input}")

                if block.name == "lookup_recent_emails":
                    result = lookup_recent_emails(
                        search_query=block.input.get("search_query"),
                        sender=block.input.get("sender"),
                        thread_id=block.input.get("thread_id"),
                        limit=block.input.get("limit", 5)
                    )
                    print(f"[Agent] Result preview: {result[:120]}...")
                elif block.name == "draft_email":
                    format_draft(block.input)
                    last_draft = block.input
                    result = "Email drafted successfully."
                else:
                    result = f"Unknown tool: {block.name}"

                print("-" * 50)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            if any(b.name == "draft_email" for b in tool_use_blocks):
                return last_draft


if __name__ == "__main__":
    print("Email Drafter — type 'quit' to exit, 'save' to save the last draft\n")
    messages = []
    last_draft = None

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        if user_input.lower() == "save":
            if last_draft:
                save_draft(last_draft)
                last_draft = None
            else:
                print("No draft to save yet.")
            continue

        print("=" * 60)
        result = run_agent(user_input, messages)
        if result is not None:
            last_draft = result
