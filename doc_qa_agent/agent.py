import os
import re
import sys
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv, find_dotenv
import anthropic

from load_pdf import load_pdf

load_dotenv(find_dotenv())

client = anthropic.Anthropic()


def save_qa(data: dict):
    os.makedirs("qa_pairs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", data["question"].lower()).strip("-")[:50]
    filename = f"qa_pairs/{timestamp}_{slug}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"**Q:** {data['question']}\n\n---\n\n{data['answer']}\n")
    print(f"[Saved] {filename}")


def run(pdf_path: str):
    print(f"\nLoading PDF...")
    pdf_data = load_pdf(pdf_path)

    print("\nDocument Q&A Agent ready. The PDF is loaded into context.")
    print("Type 'quit' to exit.\n")

    messages = []
    first_turn = True
    last_qa = None

    while True:
        try:
            question = input("Ask a question (or 'quit' to exit): ").strip()
        except EOFError:
            break

        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        if not question:
            continue

        if question.lower() == "save":
            if last_qa:
                save_qa(last_qa)
            else:
                print("Nothing to save yet.")
            continue

        # First turn: send document block + question together.
        # Subsequent turns: send plain text only — PDF stays in message[0].
        if first_turn:
            content = [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data,
                    },
                    "cache_control": {"type": "ephemeral"},
                },
                {"type": "text", "text": question},
            ]
            first_turn = False
        else:
            content = question

        messages.append({"role": "user", "content": content})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=messages,
        )

        reply = next(b.text for b in response.content if b.type == "text")
        messages.append({"role": "assistant", "content": reply})
        last_qa = {"question": question, "answer": reply}

        u = response.usage
        print(f"[Cache] write={u.cache_creation_input_tokens} "
              f"read={u.cache_read_input_tokens} "
              f"input={u.input_tokens}\n")
        print(f"Claude: {reply}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py path/to/your.pdf")
        sys.exit(1)

    try:
        run(sys.argv[1])
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye.")
