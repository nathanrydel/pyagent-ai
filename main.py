import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args.verbose)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
    )

    if not response.usage:
        raise RuntimeError("An OpenRouter error occurred, please try again")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("User prompt:", messages[0]["content"])
        print("Response tokens:", response.usage.completion_tokens)

    print("Response:", response.choices[0].message.content)


if __name__ == "__main__":
    main()
