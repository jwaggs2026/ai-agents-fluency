import os
import sys
sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv, find_dotenv
import anthropic

load_dotenv(find_dotenv())

def main():
    print("Checking environment...")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("FAIL: ANTHROPIC_API_KEY is not set.")
        print("      Copy .env.example to .env in the project root and add your key.")
        sys.exit(1)

    masked = api_key[:8] + "..." + api_key[-4:]
    print(f"  ANTHROPIC_API_KEY found: {masked}")

    print("\nConnecting to Anthropic API...")
    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=32,
            messages=[{"role": "user", "content": "Reply with the single word: OK"}],
        )
        reply = response.content[0].text.strip()
        print(f"  Smoke test response: {reply}")
        print("\nSUCCESS: Environment is ready. Run the agent with:")
        print("         python agent.py path/to/your.pdf")
    except anthropic.AuthenticationError:
        print("FAIL: API key was rejected. Check that your key is valid.")
        sys.exit(1)
    except anthropic.APIConnectionError:
        print("FAIL: Could not connect to Anthropic. Check your internet connection.")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: Unexpected error — {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
