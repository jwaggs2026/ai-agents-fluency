import sys
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

if len(sys.argv) > 1:
    user_message = " ".join(sys.argv[1:])
else:
    user_message = input("Your message: ")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    messages=[
        {"role": "user", "content": user_message}
    ],
)

print(response.content[0].text)
